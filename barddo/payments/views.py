# coding=utf-8
import datetime

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin

from accounts.views import LoginRequiredMixin, ProfileAwareView
from core.models import Work
from payments.models import Item, Purchase, PurchaseStatus, PaymentMethod
from payments.processor import PaymentProcessor


class CreatePayment(LoginRequiredMixin, TemplateResponseMixin, View):
    PENDING_ID = 1
    PAYPAL_METHOD_ID = 1

    def get(self, request):
        work_ids = request.GET.getlist('work_id', [])
        works = Work.objects.filter(id__in=work_ids)
        user = request.user
        for work in works:
            if work.is_owned_by(user):
                # FIXME: Essa validação é temporaria, o certo é quando tivermos um carrinho ter uma pagina de confirmação da compra
                # FIXME: onde essas validações serão feitas permitindo o usuário alterar o carrinho antes de finalizar a compra.
                self.template_name = 'payment_error.html'
                context = {'payment_error': _('You own this comic book!')}
                return super(CreatePayment, self).render_to_response(context)
        pending_status = PurchaseStatus.objects.get(pk=self.PENDING_ID)
        purchase = Purchase(date=datetime.datetime.now(), buyer=user, status=pending_status)
        purchase.save()

        item_list = []
        total_price = 0
        for work in works:
            work_price = work.price
            total_price += work_price
            item_list.append(Item(work=work, price=work_price, purchase=purchase))

        Item.objects.bulk_create(item_list)
        purchase.total = total_price
        purchase.save()

        processor = PaymentProcessor()
        payment_method = PaymentMethod.objects.get(pk=self.PAYPAL_METHOD_ID)
        return_url = request.build_absolute_uri(reverse('payments.paypal.execute'))
        cancel_url = request.build_absolute_uri(reverse('core.index'))
        payment = processor.create_payment(purchase, payment_method, return_url=return_url, cancel_url=cancel_url)

        request.session['payment_id'] = payment.code
        request.session['work_ids'] = work_ids
        return processor.execute_payment(payment)


class PaymentDoesNotExist(LoginRequiredMixin, ProfileAwareView):
    template_name = 'no_payments.html'


class PaymentThanks(LoginRequiredMixin, ProfileAwareView):
    template_name = 'thanks.html'

    def get(self, request, *args, **kwargs):
        kwargs['work_ids'] = request.session['work_ids']
        return super(PaymentThanks, self).get(request, *args, **kwargs)
# coding=utf-8
import datetime
import json

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.views.generic import View

from accounts.views import LoginRequiredMixin, ProfileAwareView
from core.models import Work
from payments.banks import bank_codes
from payments.models import Item, Purchase, PurchaseStatus, PaymentMethod
from payments.processor import PaymentProcessor


class CreatePayment(LoginRequiredMixin, View):
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
                messages.error(request, _('You own this comic book!'))
                return HttpResponseRedirect(reverse('payment.error'))
        pending_status = PurchaseStatus.objects.get(pk=self.PENDING_ID)
        purchase = Purchase(date=datetime.datetime.now(), buyer=user, status=pending_status)
        purchase.save()

        item_list = []
        total_price = 0
        for work in works:
            work_price = work.price
            total_price += work_price
            item_list.append(Item(work=work, price=work_price, purchase=purchase, taxes=0))

        Item.objects.bulk_create(item_list)
        purchase.total = total_price
        purchase.save()

        processor = PaymentProcessor()
        payment_method = PaymentMethod.objects.get(pk=self.PAYPAL_METHOD_ID)
        return_url = request.build_absolute_uri(reverse('payments.paypal.execute'))
        cancel_url = request.build_absolute_uri(reverse('core.index'))
        payment = processor.create_payment(purchase, payment_method, request=request, return_url=return_url, cancel_url=cancel_url)

        request.session['payment_id'] = payment.code
        request.session['work_ids'] = work_ids
        return processor.execute_payment(payment)


class PaymentDoesNotExist(LoginRequiredMixin, ProfileAwareView):
    template_name = 'no_payments.html'


class PaymentErrorView(LoginRequiredMixin, ProfileAwareView):
    template_name = 'payment_error.html'


class PaymentThanks(LoginRequiredMixin, ProfileAwareView):
    template_name = 'thanks.html'

    def get(self, request, *args, **kwargs):
        kwargs['work_ids'] = request.session['work_ids']
        return super(PaymentThanks, self).get(request, *args, **kwargs)


class BankCodeProvider(LoginRequiredMixin, View):
    """
    Provides all bank codes as JSON
    """

    def get(self, *args, **kwargs):
        banks = map(lambda bank: {'id': bank['code'], 'text': "{0}-{1}".format(bank['code'], bank['name'])}, bank_codes)
        data = json.dumps(banks)
        return HttpResponse(data, content_type='application/json')
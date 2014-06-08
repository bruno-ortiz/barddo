import datetime

from django.core.urlresolvers import reverse
from django.views.generic import View

from accounts.views import LoginRequiredMixin, ProfileAwareView
from core.models import Work
from payments.models import Item, Purchase, PurchaseStatus, PaymentMethod
from payments.processor import PaymentProcessor


class CreatePayment(LoginRequiredMixin, View):
    PENDING_ID = 1
    PAYPAL_METHOD_ID = 1

    def get(self, request):
        work_ids = request.GET.getlist('work_id', [])
        works = Work.objects.filter(id__in=work_ids)

        user = request.user
        pending_status = PurchaseStatus.objects.get(pk=self.PENDING_ID)
        purchase = Purchase(date=datetime.datetime.now(), buyer=user, status=pending_status, total=0.0)
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
        return processor.execute_payment(payment)


class PaymentDoesNotExist(LoginRequiredMixin, ProfileAwareView):
    template_name = 'no_payments.html'


class PaymentThanks(LoginRequiredMixin, ProfileAwareView):
    template_name = 'thanks.html'
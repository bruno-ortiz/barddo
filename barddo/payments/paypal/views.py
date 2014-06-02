import datetime

from django.conf import settings

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic import View
import paypalrestsdk

from payments.exceptions import PaymentError

from payments.models import Payment, PurchaseStatus, FINISHED_PURCHASE_ID


class ExecutePayment(View):
    def get(self, request):
        payer_id = request.GET.get('PayerID')

        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET})

        payment_id = request.session.get('payment_id')
        if payment_id:
            paypal_payment = paypalrestsdk.Payment.find(payment_id)
            if paypal_payment.execute({"payer_id": payer_id}):
                payment = Payment.objects.get(code=payment_id)
                payment.settled_date = datetime.datetime.now()
                purchase = payment.purchase
                purchase.status = PurchaseStatus.objects.get(pk=FINISHED_PURCHASE_ID)
                purchase.save()
                payment.save()
                return HttpResponseRedirect(reverse('core.index'))
            else:
                raise PaymentError(_('It was not possible to confirm your payment'))  # TODO: tratar erro
        else:
            raise PaymentError(_('It was not possible to confirm your payment'))  # TODO: Redirecionar para pagina especifica
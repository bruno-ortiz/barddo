# coding=utf-8
import datetime

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
import paypalrestsdk

from accounts.views import LoginRequiredMixin
from payments.models import Payment, PurchaseStatus, FINISHED_PURCHASE_ID


class ExecutePayment(LoginRequiredMixin, TemplateResponseMixin, View):
    def get(self, request):
        payment_id = request.session.get('payment_id')
        if payment_id:
            payer_id = request.GET.get('PayerID')

            paypalrestsdk.configure({
                "mode": settings.PAYPAL_MODE,
                "client_id": settings.PAYPAL_CLIENT_ID,
                "client_secret": settings.PAYPAL_CLIENT_SECRET})
            paypal_payment = paypalrestsdk.Payment.find(payment_id)
            if paypal_payment.execute({"payer_id": payer_id}):
                payment = Payment.objects.get(code=payment_id)
                payment.settled_date = datetime.datetime.now()
                payment.save()
                purchase = payment.purchase
                purchase.status = PurchaseStatus.objects.get(pk=FINISHED_PURCHASE_ID)
                purchase.save()
                return HttpResponseRedirect(reverse('payment.thanks'))
            else:
                messages.error(request, _('It was not possible to confirm your payment'))
                return HttpResponseRedirect(reverse('payment.error'))
        else:
            return HttpResponseRedirect(reverse('payment.does.not.exist'))
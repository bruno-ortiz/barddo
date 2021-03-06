# coding=utf-8
import datetime

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
import paypalrestsdk

from payments.exceptions import PaymentError
from payments.models import Payment, PaymentMethod


class PaypalProcessor(object):
    PAYPAL_METHOD_ID = 1

    def create_payment(self, purchase, **kwargs):
        """
        Cria um pagamento do paypal
        """
        items = self.__create_items(purchase)

        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET})

        paypal_payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": kwargs.get('return_url'),
                "cancel_url": kwargs.get('cancel_url')
            },
            "transactions": [{"item_list": {"items": items},
                              "amount": {"total": str(purchase.total),
                                         "currency": "BRL"},  # TODO: Detectar moeda local do usuário
                              "description": "Purchase {}".format(purchase.id)}]
        })

        if paypal_payment.create():
            payment = Payment()
            payment.code = paypal_payment.id
            payment.creation_date = datetime.datetime.now()
            payment.method = PaymentMethod.objects.get(pk=self.PAYPAL_METHOD_ID)
            payment.save()

            return payment
        raise PaymentError(_("We are sorry but your payment could not be processed!"))

    def execute_payment(self, payment, **kwargs):
        """
        executa um pagamento do paypal
        """
        redirect_url = None
        paypal_payment = paypalrestsdk.Payment.find(payment.code)
        for link in paypal_payment.links:
            if link.method == "REDIRECT":
                redirect_url = link.href
        if redirect_url is None:
            redirect_url = reverse('payment.error')
            request = kwargs['request']
            messages.error(request, _('Sorry, but an error occurred with paypal, we will verify immediately!'))
        return HttpResponseRedirect(redirect_url)

    def get_payment_status(self, payment):
        pass

    @staticmethod
    def __create_items(purchase):
        items = []
        for i in purchase.items.all():
            item = {'name': i.work.title, 'price': str(i.price), 'currency': 'BRL', 'quantity': '1'}  # TODO: detect the currency from the user
            items.append(item)
        return items
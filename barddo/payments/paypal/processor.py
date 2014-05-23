import datetime

from django.conf import settings
from django.utils.translation import ugettext as _
import paypalrestsdk

from payments.exceptions import PaymentError
from payments.models import Payment, PaymentMethod, PurchaseStatus


class PaypalProcessor(object):
    PAYPAL_METHOD_ID = 1
    PURCHASE_COMPLETED_ID = 2

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
                              "amount": {"total": purchase.total,
                                         "currency": "USD"},  # TODO: detect the currency from the user
                              "description": "Purchase {}".format(purchase.id)}]
        })

        if paypal_payment.create():
            payment = Payment()
            payment.code = paypal_payment.id
            payment.creation_date = datetime.datetime.now()
            payment.method = PaymentMethod.objects.get(pk=self.PAYPAL_METHOD_ID)
            payment.save()

            return payment
        raise PaymentError(_("We are sorry but you're payment couldn't be created!"))

    def execute_payment(self, payment, **kwargs):
        """
        executa um pagamento do paypal
        """
        payer_id = kwargs.get('payer_id')

        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET})

        paypal_payment = paypalrestsdk.Payment.find(payment.code)
        if paypal_payment.execute({"payer_id": payer_id}):
            payment.settled_date = datetime.datetime.now()
            payment.purchase.status = PurchaseStatus.objects.get(pk=self.PURCHASE_COMPLETED_ID)
        raise PaymentError(_('It was not possible to confirm your payment'))

    def get_payment_status(self, payment):
        pass

    @staticmethod
    def __create_items(purchase):
        items = []
        for i in purchase.items:
            item = {'name': i.work.title, 'price': i.price, 'currency': 'USD', 'quantity': 1}  # TODO: detect the currency from the user
            items.append(item)
        return items
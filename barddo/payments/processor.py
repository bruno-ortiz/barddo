# coding=utf-8
from payments.exceptions import PaymentError

from payments.models import Purchase
from payments.paypal.processor import PaypalProcessor

PAYMENT_METHOD_PROCESSORS = {
    1: PaypalProcessor
}


class PaymentProcessor(object):
    """
        Responsável por delegar chamadas aos processors específicos de cada método de pagamento
    """

    def create_payment(self, purchase, payment_method, **kwargs):
        """
            Delega a um processor uma requisição para criar um pagamento.
        """
        if purchase.payment is not None:
            # No futuro podemos permitir troca de forma de pagamento
            raise PaymentError('Purchase already has a payment.', payment_method.name)

        processor = self.get_processor(payment_method)

        payment = processor.create_payment(purchase, **kwargs)
        purchase.payment = payment
        purchase.save()  # Não sei se é bom fazer isso

        return payment

    def execute_payment(self, payment, **kwargs):
        """
            Delega a um processor uma requisição para executar um pagamento.
        """
        processor = self.get_processor(payment.method)
        return processor.execute_payment(payment)

    def update_payment_information(self, purchase):
        """
            Delega a um processor uma requisição para buscar o status atualizado de um pagamento.
        """
        payment = purchase.payment
        processor = self.get_processor(payment.method)

        status = processor.get_payment_status(payment)

        if purchase.status != status:
            self.notify_status_changed(payment, status)

    @staticmethod
    def notify_status_changed(payment, status):
        """
            Quando um processor específico perceber alguma alteração de status de pagamento esse método deverá ser
            chamado.
        """
        purchase = Purchase.objects.get(payment=payment)
        purchase.status = status
        purchase.save()

    @staticmethod
    def get_processor(payment_method):
        """
            Obtem o processor específico para o método de pagamento informado
        """
        processor_class = PAYMENT_METHOD_PROCESSORS[payment_method.id]

        if processor_class is None:
            # O tratamento de internacionalizacao pode ser dentro de PaymentError ou isso pode dar problema?
            raise PaymentError('Payment method processor for {} not found.', payment_method.name)

        return processor_class()
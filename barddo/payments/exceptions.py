class PaymentError(Exception):
    def __init__(self, message, *args):
        self.message = message.format(*args)
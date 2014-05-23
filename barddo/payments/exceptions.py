from django.utils.translation import ugettext as _


class PaymentError(Exception):
    def __init__(self, message, *args):
        self.message = _(message).format(*args)  # Podemos fazer isso?
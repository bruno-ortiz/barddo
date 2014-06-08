from django.conf.urls import patterns, url, include

from payments.views import CreatePayment, PaymentDoesNotExist, PaymentThanks


urlpatterns = patterns(
    '',
    url(r'^payment/create$', CreatePayment.as_view(), name='payment.create'),
    url(r'^payment/does/not/exist$', PaymentDoesNotExist.as_view(), name='payment.does.not.exist'),
    url(r'^payment/thanks$', PaymentThanks.as_view(), name='payment.thanks'),

    url(r'^', include('payments.paypal.urls')),
)
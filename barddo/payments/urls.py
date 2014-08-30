from django.conf.urls import patterns, url, include

from payments.views import CreatePayment, PaymentDoesNotExist, PaymentThanks, PaymentErrorView, BankCodeProvider


urlpatterns = patterns(
    '',
    url(r'^payment/create$', CreatePayment.as_view(), name='payment.create'),
    url(r'^payment/does/not/exist$', PaymentDoesNotExist.as_view(), name='payment.does.not.exist'),
    url(r'^payment/error$', PaymentErrorView.as_view(), name='payment.error'),
    url(r'^payment/thanks$', PaymentThanks.as_view(), name='payment.thanks'),
    url(r'^bank/codes$', BankCodeProvider.as_view(), name='bank.codes'),

    url(r'^', include('payments.paypal.urls')),
)
from django.conf.urls import patterns, url

from payments.paypal.views import ExecutePayment


urlpatterns = patterns(
    '',
    url(r'payments/paypal/execute$', ExecutePayment.as_view(), name='payments.paypal.execute'),
)
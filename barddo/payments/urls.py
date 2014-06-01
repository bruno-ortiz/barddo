from django.conf.urls import patterns, url, include

from payments.views import CreatePayment


urlpatterns = patterns(
    '',
    url(r'^payments/create$', CreatePayment.as_view(), name='payments.create'),

    url(r'^', include('payments.paypal.urls')),
)
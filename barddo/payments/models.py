from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

AUTH_USER = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class PaymentMethod(models.Model):
    name = models.CharField(_('Payment Method'), max_length=20)


class Payment(models.Model):
    code = models.CharField(max_length=30)
    date = models.DateField(db_index=True)
    method = models.ForeignKey(PaymentMethod)


class Item(models.Model):
    class Meta:
        unique_together = ('work', 'price')

    work = models.OneToOneField('core.Work')
    price = models.DecimalField(max_digits=6, decimal_places=2)


class PurchaseStatus(models.Model):
    name = models.CharField(_('Purchase Status'), max_length=20)


class Purchase(models.Model):
    date = models.DateField(db_index=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.OneToOneField(Payment)
    buyer = models.ForeignKey(AUTH_USER)
    status = models.ForeignKey(PurchaseStatus)

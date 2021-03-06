from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import BarddoUser


AUTH_USER = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
PENDING_PURCHASE_ID = 1
FINISHED_PURCHASE_ID = 2


class PaymentMethod(models.Model):
    name = models.CharField(_('Payment Method'), max_length=20)


class Payment(models.Model):
    code = models.CharField(max_length=50)
    creation_date = models.DateField(db_index=True, null=False)
    settled_date = models.DateField(db_index=True, null=True)
    method = models.ForeignKey(PaymentMethod)


class PurchaseStatus(models.Model):
    name = models.CharField(_('Purchase Status'), max_length=20)


class PurchaseManager(models.Manager):
    def is_owned_by(self, work, user):
        return self.get_queryset().filter(buyer=user, status=FINISHED_PURCHASE_ID, items__work=work).exists()


class Purchase(models.Model):
    date = models.DateTimeField(db_index=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment = models.OneToOneField(Payment, null=True)
    buyer = models.ForeignKey(AUTH_USER)
    status = models.ForeignKey(PurchaseStatus)

    objects = PurchaseManager()


class Item(models.Model):
    class Meta:
        unique_together = ('purchase', 'work')

    purchase = models.ForeignKey(Purchase, related_name='items')
    work = models.ForeignKey('core.Work', related_name='items')
    taxes = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class BankAccount(models.Model):
    user = models.OneToOneField(BarddoUser)
    favored_name = models.CharField(_('Favoured Name'), max_length=100, db_index=True)
    cpf = models.CharField(_('Social Security'), max_length=15, db_index=True)
    bank_code = models.CharField(_('Bank Code'), max_length=10)
    agency = models.CharField(_('Agency'), max_length=8)
    account = models.CharField(_('Account'), max_length=10)
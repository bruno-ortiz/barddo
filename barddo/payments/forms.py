from django.forms import ModelForm

from payments.models import BankAccount


class BankAccountForm(ModelForm):
    class Meta:
        model = BankAccount
        exclude = ('user',)
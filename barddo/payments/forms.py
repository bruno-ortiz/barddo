import re

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from payments.models import BankAccount


class BankAccountForm(ModelForm):
    PATTERN = re.compile(r'^\d+\-?\d+$')

    class Meta:
        model = BankAccount
        exclude = ('user',)

    def clean_account(self):
        account = self.cleaned_data.get('account')
        if not self.PATTERN.match(account):
            raise ValidationError(_("Account must contains only numbers or '-' separators and finish with a number."))
        return account

    def clean_agency(self):
        agency = self.cleaned_data.get('agency')
        if not self.PATTERN.match(agency):
            raise ValidationError(_("Agency must contains only numbers or '-' separators and finish with a number."))
        return agency
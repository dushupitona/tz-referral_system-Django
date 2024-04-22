from django import forms
from phonenumber_field.formfields import PhoneNumberField


class EnterPhoneNumberForm(forms.Form):
    phone_number = PhoneNumberField(region="RU")


class EnterAuthCodeForm(forms.Form):
    auth_code = forms.CharField(min_length=6, max_length=6)
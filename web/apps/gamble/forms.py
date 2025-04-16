from django import forms


class RegistrationForm(forms.Form):
    lucky_username = forms.CharField(max_length=255, label="Ваше имя")

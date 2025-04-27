from django import forms
from .models import RegisteredUser, Position
from django.core.validators import RegexValidator


class RegistrationForm(forms.ModelForm):
    """
    ModelForm for registering a new user. Includes all required fields except telegram info,
    which should be provided via hidden fields or request context.
    """

    # Скрытые поля для telegram_id и telegram_username
    telegram_id = forms.CharField(widget=forms.HiddenInput)
    telegram_username = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = RegisteredUser
        fields = [
            "telegram_id",
            "telegram_username",
            "lucky_username",
            "rest_title",
            "position",
            "phone",
            "is_subscribed",
        ]
        widgets = {
            "lucky_username": forms.TextInput(attrs={"class": "form-control"}),
            "rest_title": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.Select(
                attrs={"class": "form-select"}
            ),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }
        help_texts = {
            "phone": "Введите номер в международном формате, например +1234567890",
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        validator = RegexValidator(
            r"^\+?\d{10,15}$", "Введите корректный международный номер"
        )
        validator(phone)
        return phone

    def clean(self):
        cleaned = super().clean()
        # Здесь можно добавить дополнительную валидацию между полями
        return cleaned

from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django import forms
from django.conf import settings
import requests


# Модель для должностей (если позиций немного, можно заменить на choices)
class Position(models.Model):
    # code = models.CharField(max_length=50, unique=True, verbose_name="Код должности")
    name = models.CharField(max_length=100, verbose_name="Название должности")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


# Основная модель пользователя
class RegisteredUser(models.Model):
    telegram_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Telegram ID",
    )
    telegram_username = models.CharField(
        max_length=255,
        verbose_name="Telegram Username",
    )
    lucky_username = models.CharField(max_length=255, verbose_name="Lucky Username")
    rest_title = models.CharField(max_length=168, verbose_name="Название ресторана")
    phone = models.CharField(
        max_length=16,
        unique=True,
        verbose_name="Телефонный номер",
        help_text="Введите номер в международном формате, например +1234567890",
        validators=[
            validators.RegexValidator(
                r"^\+?\d{10,15}$", "Введите корректный международный номер"
            )
        ],
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Должность",
    )
    is_subscribed = models.BooleanField(verbose_name="Подписан на канал")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    def __str__(self):
        return f"{self.lucky_username} (@{self.telegram_username.lstrip('@')})"

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

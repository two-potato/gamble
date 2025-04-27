import logging
from django.views.generic import TemplateView, CreateView
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import RegistrationForm
from .models import RegisteredUser

logger = logging.getLogger(__name__)


class RegisterView(CreateView):
    """
    Регистрация пользователя из Telegram Web App.
    До показа/сохранения — проверяем GET['is_subscribed'] и
    наличе записи telegram_id.
    """

    model = RegisteredUser
    form_class = RegistrationForm
    template_name = "index.html"
    success_url = reverse_lazy("gamble:success")
    
    

    def dispatch(self, request, *args, **kwargs):
        # 1) Проверяем, передал ли бот is_subscribed=1
        if request.GET.get("is_subscribed") != "1":
            messages.error(
                request, "Чтобы участвовать в розыгрыше, подпишитесь на наш канал."
            )
            return redirect(reverse_lazy("gamble:not_subscribed"))

        # 2) Берём telegram_id из GET
        telegram_id = request.GET.get("telegram_id")
        if not telegram_id:
            messages.error(request, "Нет данных о вашем Telegram ID.")
            return redirect(reverse_lazy("gamble:error"))

        # 3) Если уже есть запись — сразу на already_subscribed
        if RegisteredUser.objects.filter(telegram_id=telegram_id).exists():
            messages.info(request, "Вы уже участвуете в розыгрыше.")
            return redirect(reverse_lazy("gamble:already_subscribed"))

        # Иначе — вперёд к GET/POST формы
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        # Предзаполняем скрытые поля формы данными из GET
        return {
            "telegram_id": self.request.GET.get("telegram_id"),
            "telegram_username": self.request.GET.get("telegram_username", ""),
            "is_subscribed": self.request.GET.get("is_subscribed", "0"),
        }

    def form_valid(self, form):
        # Дополнительно ещё раз убеждаемся, что is_subscribed=1
        is_subscribed = self.request.GET.get("is_subscribed")
        if is_subscribed != "1":
            messages.error(self.request, "Подписка на канал не обнаружена.")
            return redirect(reverse_lazy("gamble:not_subscribed"))

        # Сохраняем форму, дописывая telegram-поля
        obj = form.save(commit=False)
        obj.telegram_id = self.request.GET["telegram_id"]
        obj.telegram_username = self.request.GET.get("telegram_username", "")
        obj.is_subscribed = is_subscribed
        obj.save()

        messages.success(self.request, "Регистрация прошла успешно!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)


class SuccessView(TemplateView):
    template_name = "success.html"


class PrivatPolicyView(TemplateView):
    template_name = "private_policy.html"


class NotSubscribedView(TemplateView):
    template_name = "not_subscribed.html"


class AlreadySubscribedView(TemplateView):
    template_name = "already_subscribed.html"


# REST API
from rest_framework import generics
from .serializers import RegisteredUserSerializer


class RegisteredUserList(generics.ListAPIView):
    queryset = RegisteredUser.objects.all()
    serializer_class = RegisteredUserSerializer

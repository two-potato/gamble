import json
from urllib.parse import unquote
from django.views.generic import View
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import RegisteredUser
from rest_framework import generics
from .serializers import RegisteredUserSerializer
from .forms import RegistrationForm


class RegisterView(View):
    template_name = "index.html"

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            telegram_id = request.POST.get("telegram_id")
            if not telegram_id:
                return JsonResponse(
                    {"status": "error", "message": "Invalid Telegram ID"}
                )
            telegram_username = request.POST.get("telegram_username")
            # telegram_username = "John"
            if not telegram_username:
                return JsonResponse(
                    {"status": "error", "message": "Invalid Telegram Username"}
                )

            lucky_username = form.cleaned_data["lucky_username"]

            if RegisteredUser.objects.filter(telegram_id=telegram_id).exists():
                return JsonResponse(
                    {"status": "error", "message": "Пользователь уже зарегистрирован"}
                )

            RegisteredUser.objects.create(
                telegram_id=telegram_id,
                telegram_username=telegram_username,
                lucky_username=lucky_username,
            )
            return JsonResponse({"status": "success"})
        return render(request, self.template_name, {"form": form})


class RegisteredUserList(generics.ListAPIView):
    queryset = RegisteredUser.objects.all()
    serializer_class = RegisteredUserSerializer

from django.contrib import admin
from .models import RegisteredUser


@admin.register(RegisteredUser)
class RegisteredUserAdmin(admin.ModelAdmin):

    list_display = (
        "telegram_id",
        "lucky_username",
    )

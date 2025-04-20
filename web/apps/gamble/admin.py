from django.contrib import admin
from .models import RegisteredUser, Position


@admin.register(RegisteredUser)
class RegisteredUserAdmin(admin.ModelAdmin):

    list_display = (
        "telegram_id",
        "telegram_username",
        "lucky_username",
        "rest_title",
        "position",
        "phone",
        "is_subscribed",
        "created_at",
    )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):

    list_display = ("name",)

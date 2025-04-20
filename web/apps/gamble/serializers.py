from rest_framework import serializers
from .models import RegisteredUser


class RegisteredUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredUser
        fields = [
            "telegram_id",
            "telegram_username",
            "lucky_username",
            "rest_title",
            "phone",
            "position",
            "is_subscribed",
            "created_at",
        ]

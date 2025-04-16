from rest_framework import serializers
from .models import RegisteredUser


class RegisteredUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredUser
        fields = ["telegram_id", "lucky_username"]

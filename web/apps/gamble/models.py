from django.db import models


class RegisteredUser(models.Model):
    telegram_id = models.CharField(max_length=255)
    lucky_username = models.CharField(max_length=255)

    def __str__(self):
        return self.lucky_username

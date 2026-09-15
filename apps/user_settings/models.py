from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    dark_mode = models.BooleanField(default=False)
    email_notif = models.BooleanField(default=True)

    def __str__(self):
        return f"Settings for {self.user.username}"
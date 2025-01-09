from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import random

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)


class OTP(models.Model):
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def generate_otp(self):
        self.otp_code = str(random.randint(100000, 999999))
        self.save()
    
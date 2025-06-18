from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class MyUser(AbstractUser):
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):  # Kiểm tra xem password đã hash chưa
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
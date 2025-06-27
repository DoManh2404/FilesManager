from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Create your models here.
class MyUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):  # Kiểm tra xem password đã hash chưa
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        permissions = [
            ("can_delete_file", "Can delete file"),
            ("can_download_file", "Can download file"),
        ]

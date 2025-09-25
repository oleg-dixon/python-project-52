from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )

    USERNAME_FIELD = 'username'
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


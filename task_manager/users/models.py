from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _

from .validators import username_validator


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_('Имя пользователя'),
        validators=[username_validator],
        error_messages={
            'unique': _("Пользователь с таким именем уже существует."),
        },
    )
    first_name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        verbose_name=_('Имя')
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name=_('Фамилия')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Дата обновления')
    )

    USERNAME_FIELD = 'username'
    
    def __str__(self):
        return self.username
    
    def get_local_created_at(self):
        return localtime(self.created_at)
    
    def get_local_updated_at(self):
        return localtime(self.updated_at)
    
    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

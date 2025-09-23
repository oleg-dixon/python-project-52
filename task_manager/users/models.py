from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _

from .validators import username_validator


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('В поле "Имя пользователя" должно быть задано'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
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
    password = models.CharField(
        max_length=128, verbose_name=_('Пароль')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Дата обновления')
    )
    
    is_active = models.BooleanField(
        default=True, verbose_name=_('Активен')
    )
    is_staff = models.BooleanField(
        default=False, verbose_name=_('Сотрудник')
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.username
    
    def get_local_created_at(self):
        return localtime(self.created_at)
    
    def get_local_updated_at(self):
        return localtime(self.updated_at)
    
    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

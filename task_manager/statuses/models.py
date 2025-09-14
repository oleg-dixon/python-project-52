from django.db import models
from django.utils.timezone import localtime
from django.conf import settings


class Status(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название статуса'
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_statuses',
        verbose_name='Создатель'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_local_created_at(self):
        return localtime(self.created_at)

    def get_local_updated_at(self):
        return localtime(self.updated_at)

    class Meta:
        db_table = 'statuses'
        verbose_name = 'статус'
        verbose_name_plural = 'статусы'

from django.db import models
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_('Название статуса')
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
        verbose_name = _('статус')
        verbose_name_plural = _('статусы')

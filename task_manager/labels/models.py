from django.db import models
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_('Название метки')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )

    def __str__(self):
        return self.name

    def get_local_created_at(self):
        return localtime(self.created_at)

    def get_local_updated_at(self):
        return localtime(self.updated_at)

    class Meta:
        db_table = 'labels'
        verbose_name = _('метка')
        verbose_name_plural = _('метки')

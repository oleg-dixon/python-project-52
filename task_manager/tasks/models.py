from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Название задачи')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Описание')
    )
    status = models.ForeignKey(
        'statuses.Status',
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name=_('Статус')
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_tasks',
        verbose_name=_('Автор')
    )
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='assigned_tasks',
        blank=True,
        null=True,
        verbose_name=_('Исполнитель')
    )
    labels = models.ManyToManyField(
        'labels.Label',
        blank=True,
        related_name='tasks',
        verbose_name=_('Метки')
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

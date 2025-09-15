from django.db import models
from django.utils.timezone import localtime
from django.conf import settings


class Task(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название задачи'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    status = models.ForeignKey(
        'statuses.Status',
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name='Статус'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_tasks',
        verbose_name='Автор'
    )
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='assigned_tasks',
        blank=True,
        null=True,
        verbose_name='Исполнитель'
    )
    tags = models.ManyToManyField(
        'tags.Tag',
        blank=True,
        related_name='tasks',
        verbose_name='Метки'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    def get_local_created_at(self):
        return localtime(self.created_at)

    def get_local_updated_at(self):
        return localtime(self.updated_at)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tasks'
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'

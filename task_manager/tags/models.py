from django.db import models
from django.utils.timezone import localtime
from django.conf import settings


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название метки'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    def __str__(self):
        return self.name

    def get_local_created_at(self):
        return localtime(self.created_at)

    def get_local_updated_at(self):
        return localtime(self.updated_at)

    class Meta:
        db_table = 'tags'
        verbose_name = 'метка'
        verbose_name_plural = 'метки'

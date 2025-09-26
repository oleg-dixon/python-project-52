from django.db import models
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(
        CustomUser, 
        on_delete=models.PROTECT,
        related_name='authored_tasks'
    )
    executor = models.ForeignKey(
        CustomUser, 
        on_delete=models.PROTECT,
        null=True, 
        blank=True, 
        related_name='executed_tasks'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='task_set'
    )
    labels = models.ManyToManyField(
        Label,
        related_name='tasks',
        blank=True,
        verbose_name='Метки'
    )
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
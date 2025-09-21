from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User

from .models import Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        required=True,
        label=_('Название задачи'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Введите название задачи')
            }
        )
    )

    description = forms.CharField(
        required=False,
        label=_('Описание'),
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': _('Введите описание задачи'),
                'rows': 4
            }
        )
    )

    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=True,
        label=_('Статус'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_('Исполнитель'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label=_('Метки'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label=_('Статус'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_('Исполнитель'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    labels = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label=_('Метки'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    self_tasks = forms.BooleanField(
        required=False,
        label=_('Только мои задачи'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
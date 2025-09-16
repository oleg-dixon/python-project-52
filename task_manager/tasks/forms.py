from django import forms
from django.contrib.auth import get_user_model
from .models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.tags.models import Tag

User = get_user_model()


class TaskForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        required=True,
        label='Название задачи',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите название задачи'
            }
        )
    )

    description = forms.CharField(
        required=False,
        label='Описание',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание задачи',
                'rows': 4
            }
        )
    )

    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=True,
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label='Исполнитель',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label='Метки',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'tags']


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label='Исполнитель',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    author = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label='Автор',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label='Метки',
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )
    self_tasks = forms.BooleanField(
        required=False,
        label='Только мои задачи',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
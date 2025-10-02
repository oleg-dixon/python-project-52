from django import forms
from django.contrib.auth import get_user_model

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    executor = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        label='Исполнитель',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    label = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label='Метка',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    self_tasks = forms.BooleanField(
        required=False,
        label='Только свои задачи',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class TaskForm(forms.ModelForm):
    name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя'
        })
    )
    description = forms.CharField(
        label="Описание",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Описание',
            'rows': 3
        }),
        required=False
    )
    status = forms.ModelChoiceField(
        label="Статус",
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    executor = forms.ModelChoiceField(
        label="Исполнитель",
        queryset=get_user_model().objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    labels = forms.ModelMultipleChoiceField(
        label="Метки",
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'executor',
            'labels'
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        task = super().save(commit=False)
        if self.user:
            task.author = self.user
        if commit:
            task.save()
            self.save_m2m()
        return task
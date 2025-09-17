from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {'name': _('Название статуса')}
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Введите название статуса')
            }),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        qs = Status.objects.filter(name=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(_("Статус с таким названием уже существует."))
        return name

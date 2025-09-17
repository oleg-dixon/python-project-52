from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        labels = {
            'name': _('Название метки')
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Введите название метки')
            }),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        qs = Label.objects.filter(name=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                _("Метка с таким названием уже существует")
            )
        return name

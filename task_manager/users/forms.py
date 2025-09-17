from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User
from .validators import username_validator


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Имя пользователя"),
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": _("Введите имя пользователя")
        })
    )
    password = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": _("Введите пароль")
        })
    )


class BaseUserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=200,
        required=True,
        label=_('Имя'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите имя')
        })
    )
    
    last_name = forms.CharField(
        max_length=200,
        required=True,
        label=_('Фамилия'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите фамилию')
        })
    )
    
    username = forms.CharField(
        max_length=150,
        required=True,
        label=_('Имя пользователя'),
        validators=[username_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите имя пользователя')
        }),
        help_text=_('Обязательное поле. '
                ' Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.')
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class UserCreateForm(BaseUserForm):
    password = forms.CharField(
        required=True,
        min_length=3,
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите пароль')
        }),
        help_text=_('Ваш пароль должен содержать как минимум 3 символа.')
    )
    
    password_confirm = forms.CharField(
        required=True,
        label=_('Подтверждение пароля'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Подтвердите пароль')
        }),
        help_text=_('Для подтверждения введите, пожалуйста, пароль ещё раз.')
    )

    class Meta(BaseUserForm.Meta):
        fields = BaseUserForm.Meta.fields + ['password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError(_("Пароли не совпадают"))
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

class UserUpdateForm(BaseUserForm):

    new_password = forms.CharField(
        required=False,
        min_length=3,
        label=_('Новый пароль'),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': _('Введите новый пароль')}
        ),
        help_text=_('Оставьте пустым, если не хотите менять пароль.'),
    )

    new_password_confirm = forms.CharField(
        required=False,
        label=_('Подтверждение нового пароля'),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': _('Подтвердите новый пароль')}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        password_confirm = cleaned_data.get("new_password_confirm")
        if password and password != password_confirm:
            raise ValidationError(_("Новый пароль и подтверждение не совпадают"))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("new_password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User
from task_manager.mixins import PasswordMixin


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
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите имя пользователя')
        }),
        help_text=_('Обязательное поле. '
                'Не более 150 символов. '
                'Только буквы, цифры и символы @/./+/-/_.')
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class UserCreateForm(BaseUserForm, PasswordMixin):
    password_field_name = 'password'
    password_confirm_field_name = 'password_confirm'
    mismatch_error_message = _("Пароли не совпадают")
    
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
        self.clean_passwords()
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        return self.save_password(user, commit=commit)
    

class UserUpdateForm(BaseUserForm, PasswordMixin):
    password_field_name = 'new_password'
    password_confirm_field_name = 'new_password_confirm'
    mismatch_error_message = _("Новый пароль и подтверждение не совпадают")

    new_password = forms.CharField(
        required=False,
        min_length=3,
        label=_('Новый пароль'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Введите новый пароль')
            }
        ),
        help_text=_('Оставьте пустым, если не хотите менять пароль.'),
    )

    new_password_confirm = forms.CharField(
        required=False,
        label=_('Подтверждение нового пароля'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Подтвердите новый пароль')
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        self.clean_passwords()
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        return self.save_password(user, commit=commit)


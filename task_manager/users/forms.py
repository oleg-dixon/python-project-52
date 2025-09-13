from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User
from .validators import username_validator


class BaseUserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=200,
        required=True,
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя'
        })
    )
    
    last_name = forms.CharField(
        max_length=200,
        required=True,
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите фамилию'
        })
    )
    
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Имя пользователя',
        validators=[username_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        }),
        help_text='Обязательное поле. '
                ' Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if hasattr(self, 'instance') and self.instance.pk:
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Пользователь с таким именем уже существует.')
        else:
            if User.objects.filter(username=username).exists():
                raise ValidationError('Пользователь с таким именем уже существует.')
        return username


class UserCreateForm(BaseUserForm):
    password = forms.CharField(
        required=True,
        min_length=3,
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }),
        help_text='Ваш пароль должен содержать как минимум 3 символа.'
    )
    
    password_confirm = forms.CharField(
        required=True,
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        }),
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.'
    )

    class Meta(BaseUserForm.Meta):
        fields = BaseUserForm.Meta.fields + ['password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Пароли не совпадают")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

class UserUpdateForm(BaseUserForm):
    password = ReadOnlyPasswordHashField(
        label="Пароль",
        help_text=(
            "Пароли хранятся в зашифрованном виде. "
            "Чтобы изменить пароль, используйте поле ниже."
        ),
    )

    new_password = forms.CharField(
        required=False,
        min_length=3,
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите новый пароль'}
        ),
        help_text='Оставьте пустым, если не хотите менять пароль.',
    )

    new_password_confirm = forms.CharField(
        required=False,
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Подтвердите новый пароль'}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        password_confirm = cleaned_data.get("new_password_confirm")
        if password and password != password_confirm:
            raise ValidationError("Новый пароль и подтверждение не совпадают")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("new_password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


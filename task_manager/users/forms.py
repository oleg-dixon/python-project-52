from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class BootstrapMixin:
    def add_bootstrap(self):
        for field_name, field in self.fields.items():
            css_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{css_class} form-control'.strip()
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'


class RegisterUserForm(UserCreationForm, BootstrapMixin):
    first_name = forms.CharField(
        label="Имя",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Имя'})
    )
    last_name = forms.CharField(
        label="Фамилия",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия'})
    )
    username = forms.CharField(
        label="Имя пользователя",
        help_text=(
            "Обязательное поле. Не более 150 символов. "
            "Только буквы, цифры и символы @/./+/-/_."
        ),
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'})
    )
    password1 = forms.CharField(
        label="Пароль",
        help_text="Ваш пароль должен содержать как минимум 3 символа.",
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
        required=True
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз.",
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Подтверждение пароля'}
        ),
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'password1', 'password2'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_bootstrap()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует")
        return username


class LoginUserForm(AuthenticationForm, BootstrapMixin):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_bootstrap()


class UserEditForm(forms.ModelForm, BootstrapMixin):
    first_name = forms.CharField(
        label="Имя",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Имя'})
    )
    last_name = forms.CharField(
        label="Фамилия",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия'})
    )
    username = forms.CharField(
        label="Имя пользователя",
        help_text=(
            "Обязательное поле. Не более 150 символов. "
            "Только буквы, цифры и символы @/./+/-/_."
        ),
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'})
    )
    password1 = forms.CharField(
        label="Пароль",
        help_text="Ваш пароль должен содержать как минимум 3 символа.",
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
        required=True
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз.",
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Подтверждение пароля'}
        ),
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_bootstrap()

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if not password1 or not password2:
            raise ValidationError(
                "Пароль обязателен для изменения пользователя!"
            )
        if password1 != password2:
            raise ValidationError("Пароли не совпадают!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        user.set_password(password)
        if commit:
            user.save()
        return user

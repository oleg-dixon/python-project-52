from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserCreateForm, UserUpdateForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreateForm
    form = UserUpdateForm
    model = User

    list_display = [
        'username',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
    ]

    search_fields = ['username', 'first_name', 'last_name']

    list_filter = [
        'is_staff',
        'is_superuser',
        'is_active',
    ]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name'),
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        (_('Important dates'), {
            'fields': ('last_login',),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'first_name',
                'last_name',
                'password',
                'password_confirm',
            ),
        }),
    )

    readonly_fields = ['last_login']

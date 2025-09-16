from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect

from .models import User
from .forms import UserCreateForm, UserUpdateForm, CustomLoginForm
from task_manager.mixins import (
    UserUpdatePermissionMixin,
    UserDeletePermissionMixin,
    ContextActionMixin
)


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    ordering = ['id']


class UserCreateView(SuccessMessageMixin, ContextActionMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пользователь успешно зарегистрирован'
    action = 'create'


class UserUpdateView(UserUpdatePermissionMixin, SuccessMessageMixin, ContextActionMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:index')
    success_message = 'Пользователь успешно изменен'
    action = 'update'


class UserDeleteView(UserDeletePermissionMixin, SuccessMessageMixin, ContextActionMixin, DeleteView):
    model = User
    template_name = 'users/user_form.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users:index')
    success_message = 'Пользователь успешно удален'
    action = 'delete'

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if user.created_tasks.exists() or user.assigned_tasks.exists():
            messages.error(
                request,
                'Невозможно удалить пользователя, потому что он используется'
            )
            return redirect('users:index')
        return super().post(request, *args, **kwargs)

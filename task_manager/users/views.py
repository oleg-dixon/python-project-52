from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import UserPermissionMixin
from .models import User
from .forms import UserCreateForm, UserUpdateForm
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm


class IndexView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    ordering = ['id']


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пользователь успешно зарегистрирован'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        return context
    

class UserUpdateView(UserPermissionMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:index')
    success_message = 'Пользователь успешно изменен'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        return context


class UserDeleteView(UserPermissionMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_form.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users:index')
    success_message = 'Пользователь успешно удален'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'delete'
        return context
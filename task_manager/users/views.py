from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Users
from .forms import UserCreateForm, UserUpdateForm


class UserPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('login')

    def test_func(self):
        user = self.get_object()
        return self.request.user == user
    
    def handle_no_permission(self):
        from django.contrib import messages
        from django.shortcuts import redirect
        
        messages.error(
            self.request, 
            'У вас нет прав для изменения другого пользователя.'
        )
        return redirect('users:index')
    


class IndexView(ListView):
    model = Users
    template_name = 'users/index.html'
    context_object_name = 'users'
    ordering = ['id']


class UserCreateView(SuccessMessageMixin, CreateView):
    model = Users
    form_class = UserCreateForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пользователь успешно зарегистрирован'
    

class UserUpdateView(UserPermissionMixin, SuccessMessageMixin, UpdateView):
    model = Users
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:index')
    success_message = 'Пользователь успешно изменен'


class UserDeleteView(UserPermissionMixin, SuccessMessageMixin, DeleteView):
    model = Users
    template_name = 'users/delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users:index')
    success_message = 'Пользователь успешно удален'
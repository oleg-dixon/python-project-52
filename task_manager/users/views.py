from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.db.models import ProtectedError, Value
from django.db.models.functions import Concat
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    View,
)

from task_manager.mixins import LoginRequiredMixin
from task_manager.users.models import CustomUser

from .forms import LoginUserForm, RegisterUserForm, UserEditForm


class UserView(ListView):
    model = CustomUser
    template_name = 'users/index.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return CustomUser.objects.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).values(
            'id', 
            'username', 
            'full_name', 
            'date_joined'
        ).order_by('date_joined')


class RegistrationView(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return super().form_valid(form)


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Вы залогинены')
        return response

    def get_success_url(self):
        return reverse_lazy('main_page')


class LogoutUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        messages.info(request, 'Вы разлогинены')
        logout(request)
        return redirect('main_page')


class UserEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserEditForm
    template_name = 'users/edit.html'
    success_url = reverse_lazy('users:users')

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user.pk != user.pk:
            messages.error(
                request,
                'У вас нет прав для изменения другого пользователя'
            )
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.pk == self.object.pk:
            update_session_auth_hash(self.request, self.object)
        messages.success(self.request, 'Пользователь успешно изменен')
        return response
    

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:users')

    def get(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().pk:
            messages.error(
                request, 'У вас нет прав для изменения другого пользователя.'
            )
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.pk != self.get_object().pk:
            messages.error(
                self.request,
                'У вас нет прав для изменения другого пользователя.'
            )
            return redirect(self.success_url)
        
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Пользователь успешно удален')
            return response
        except ProtectedError:
            messages.error(
                self.request,
                'Невозможно удалить пользователя, потому что он используется'
            )
            return redirect(self.success_url)
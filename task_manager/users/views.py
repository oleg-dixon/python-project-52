from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db.models import Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View

from task_manager.mixins import LoginRequiredMixin
from task_manager.users.models import CustomUser

from .forms import LoginUserForm, RegisterUserForm, UserEditForm


class UserView(LoginRequiredMixin, ListView):
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


class RegistrationView(LoginRequiredMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return super().form_valid(form)


class LoginUserView(LoginRequiredMixin, LoginView):
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
    
    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        if self.request.user.id != user.pk:
            messages.error(
                self.request, 
                'У вас нет прав для изменения другого пользователя'
                )
            return None
        return user
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect(self.success_url)
        messages.success(request, 'Пользователь успешно изменен')
        return redirect(self.success_url)


class UserDeleteView(LoginRequiredMixin, View):
    success_url = reverse_lazy('users:users')
    template_name = 'users/user_confirm_delete.html'

    def get_object(self):
        user_id = self.kwargs.get('pk')
        return get_object_or_404(CustomUser, pk=user_id)

    def get(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if request.user.pk != user_to_delete.pk:
            messages.error(
                request, 'У вас нет прав для изменения другого пользователя.'
            )
            return redirect(self.success_url)
        return render(request, self.template_name, {'user': user_to_delete})

    def post(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if request.user.pk != user_to_delete.pk:
            messages.error(
                request, 'У вас нет прав для изменения другого пользователя.'
            )
            return redirect(self.success_url)
        user_to_delete.delete()
        messages.success(request, 'Пользователь успешно удален')
        return redirect(self.success_url)
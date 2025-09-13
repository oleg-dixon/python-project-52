# task_manager/mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy


class UserPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('users:login')

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для изменения другого пользователя.')
        return redirect('users:index')


class TaskPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('users:login')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для изменения чужой задачи.')
        return redirect('tasks:index')

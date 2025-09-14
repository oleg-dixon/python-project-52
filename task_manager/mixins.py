from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy


class UserPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('users:login')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        user = self.get_object()
        return self.request.user == user

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для изменения этого пользователя.')
        return redirect('users:index')


class TaskUpdatePermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('users:login')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        task = self.get_object()
        return (
            self.request.user == task.author
            or self.request.user == task.executor
        )

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для изменения этой задачи.')
        return redirect('tasks:index')
    

class TaskDeletePermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('users:login')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для удаления этой задачи.')
        return redirect('tasks:index')


class StatusPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('users:login')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        status = self.get_object()
        return status.creator == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для изменения этого статуса.')
        return redirect('statuses:index')


class TagPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('users:login')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        tag = self.get_object()
        return tag.creator == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для изменения этой метки.')
        return redirect('tags:index')

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import activate
from django.utils.translation import gettext_lazy as _


class ContextActionMixin:
    """Добавляет 'action' в контекст для шаблона."""
    action = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.action:
            context['action'] = self.action
        return context


class DeleteProtectMixin(LoginRequiredMixin):
    """
    Универсальный миксин для DeleteView,
    который проверяет наличие связанных объектов
    и предотвращает удаление, если объект используется.
    """
    login_url = reverse_lazy('users:login')
    protected_related_names = []
    redirect_url = None
    error_message = _('Невозможно удалить объект, потому что он используется')

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        for related_name in self.protected_related_names:
            related_manager = getattr(obj, related_name, None)
            if related_manager and related_manager.exists():
                messages.error(request, self.error_message)
                return redirect(self.redirect_url)
        return super().post(request, *args, **kwargs)


class UserUpdatePermissionMixin(LoginRequiredMixin):
    """
    Миксин для редактирования пользователя.
    Редактировать можно только самого себя.
    """
    login_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            messages.error(
                request,
                _('У вас нет прав для изменения этого пользователя.')
            )
            return redirect('users:index')
        return super().dispatch(request, *args, **kwargs)


class UserDeletePermissionMixin(LoginRequiredMixin):
    """
    Миксин для удаления пользователя.
    Удалять можно только самого себя и только если он не участвует в задачах.
    """
    login_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            messages.error(
                request,
                _('У вас нет прав для удаления этого пользователя.')
            )
            return redirect('users:index')
        if user.created_tasks.exists() or user.assigned_tasks.exists():
            messages.error(
                request,
                _('Невозможно удалить пользователя, потому что он используется в задачах.')
            )
            return redirect('users:index')
        return super().dispatch(request, *args, **kwargs)


class TaskPermissionMixin(LoginRequiredMixin):
    """
    Миксин для проверки прав на удаление задач.
    Все залогиненные пользователи могут создавать,
    редактировать и просматривать задачи.
    Удалять задачу может только автор или исполнитель.
    """
    login_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if request.method.lower() in ['post', 'put', 'patch', 'delete']:
            if request.user != task.author:
                messages.error(
                    request,
                    _('У вас нет прав для удаления этой задачи.')
                )
                return redirect('tasks:index')
        return super().dispatch(request, *args, **kwargs)


class StatusPermissionMixin(LoginRequiredMixin):
    """
    Миксин для проверки прав на удаление статуса.
    Все залогиненные пользователи могут создавать и редактировать статусы.
    Удаление невозможно, если статус используется в задачах.
    """
    login_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        status = self.get_object()
        if request.method.lower() == 'post':
            if hasattr(status, 'tasks') and status.tasks.exists():
                messages.error(
                    request,
                    _('Невозможно удалить статус, потому что он используется в задаче.')
                )
                return redirect('statuses:index')
        return super().dispatch(request, *args, **kwargs)


class LabelPermissionMixin(LoginRequiredMixin):
    """
    Миксин для проверки прав на удаление метки.
    Все залогиненные пользователи могут создавать и редактировать метки.
    Удаление невозможно, если метка используется в задачах.
    """
    login_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        label = self.get_object()
        if request.method.lower() == 'post':
            if hasattr(label, 'tasks') and label.tasks.exists():
                messages.error(
                    request,
                    _('Невозможно удалить метку, потому что она используется в задаче.')
                )
                return redirect('labels:index')
        return super().dispatch(request, *args, **kwargs)


class LanguageMixin:
    """Миксин для автоматической активации нужного языка в тестах."""
    LANGUAGE_CODE = 'ru'

    def setUp(self):
        super().setUp()
        activate(self.LANGUAGE_CODE)
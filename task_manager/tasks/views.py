from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import TaskForm
from task_manager.mixins import (
    TaskUpdatePermissionMixin,
    TaskDeletePermissionMixin
)


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    ordering = ['id']


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:index')
    success_message = 'Задача успешно создана'
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class TaskUpdateView(TaskUpdatePermissionMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:index')
    success_message = 'Задача успешно изменена'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        return context


class TaskDeleteView(TaskDeletePermissionMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:index')
    success_message = 'Задача успешно удалена'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'delete'
        return context

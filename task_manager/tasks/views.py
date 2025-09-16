from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Task
from .forms import TaskForm
from task_manager.mixins import TaskPermissionMixin, ContextActionMixin


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    ordering = ['id']


class TaskCreateView(SuccessMessageMixin, ContextActionMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:index')
    success_message = 'Задача успешно создана'
    action = 'create'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(TaskPermissionMixin, SuccessMessageMixin, ContextActionMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:index')
    success_message = 'Задача успешно изменена'
    action = 'update'


class TaskDeleteView(TaskPermissionMixin, SuccessMessageMixin, ContextActionMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:index')
    success_message = 'Задача успешно удалена'
    action = 'delete'

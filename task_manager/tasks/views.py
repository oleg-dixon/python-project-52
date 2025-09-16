from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Task
from .forms import TaskForm, TaskFilterForm
from task_manager.mixins import LoginRequiredMixin, TaskPermissionMixin, ContextActionMixin


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    ordering = ['id']

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TaskFilterForm(self.request.GET)

        if form.is_valid():
            status = form.cleaned_data.get('status')
            executor = form.cleaned_data.get('executor')
            author = form.cleaned_data.get('author')
            tags = form.cleaned_data.get('tags')
            self_tasks = form.cleaned_data.get('self_tasks')

            if status:
                queryset = queryset.filter(status=status)
            if executor:
                queryset = queryset.filter(executor=executor)
            if author:
                queryset = queryset.filter(author=author)
            if tags:
                queryset = queryset.filter(tags__in=tags).distinct()
            if self_tasks:
                queryset = queryset.filter(author=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET or None)
        return context


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

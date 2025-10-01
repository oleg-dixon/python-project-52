from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView, View

from task_manager.mixins import LoginRequiredMixin

from .forms import TaskFilterForm, TaskForm
from .models import Task


class TaskView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.select_related(
            'status',
            'author',
            'executor'
        ).order_by('time_create')
        
        status = self.request.GET.get('status')
        executor = self.request.GET.get('executor')
        label = self.request.GET.get('label')
        self_tasks = self.request.GET.get('self_tasks')
        
        if status and status != '':
            queryset = queryset.filter(status_id=int(status))
        
        if executor is not None:
            if executor == '':
                queryset = queryset.filter(executor__isnull=True)
            else:
                queryset = queryset.filter(executor_id=int(executor))
        
        if label and label != '':
            queryset = queryset.filter(labels__id=label).distinct()
        
        if self_tasks and self_tasks.lower() in ['true', 'on', '1', 'yes']:
            queryset = queryset.filter(author=self.request.user)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET)
        return context


class CreateTaskView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TaskForm(user=request.user)
        return render(request, 'tasks/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно создана')
            return redirect('tasks:tasks')
        return render(request, 'tasks/create.html', {'form': form})


class ShowTaskView(LoginRequiredMixin, View):
    def get_object(self):
        task_id = self.kwargs.get('task_id')
        return get_object_or_404(Task, pk=task_id)

    def get(self, request, *args, **kwargs):
        task_to_show = self.get_object()
        return render(request, 'tasks/show_task.html', {'task': task_to_show})


class EditTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/edit.html'
    success_url = reverse_lazy('tasks:tasks')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно изменена')
        return super().form_valid(form)


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:tasks')

    def get(self, request, *args, **kwargs):
        if request.user.id != self.get_object().author.id:
            messages.error(request, 'Задачу может удалить только ее автор')
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.id != self.get_object().author.id:
            messages.error(self.request, 'Задачу может удалить только ее автор')
            return redirect(self.success_url)
        
        response = super().form_valid(form)
        messages.success(self.request, 'Задача успешно удалена')
        return response
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Status
from .forms import StatusForm
from task_manager.mixins import StatusPermissionMixin, DeleteProtectMixin, ContextActionMixin


class StatusListView(ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'
    ordering = ['id']


class StatusCreateView(SuccessMessageMixin, ContextActionMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:index')
    success_message = 'Статус успешно создан'
    action = 'create'


class StatusUpdateView(StatusPermissionMixin, SuccessMessageMixin, ContextActionMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:index')
    success_message = 'Статус успешно изменен'
    action = 'update'


class StatusDeleteView(StatusPermissionMixin, DeleteProtectMixin, SuccessMessageMixin, ContextActionMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:index')
    success_message = 'Статус успешно удален'
    redirect_url = reverse_lazy('statuses:index')
    protected_related_names = ['tasks']
    action = 'delete'

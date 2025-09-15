from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Status
from .forms import StatusForm
from task_manager.mixins import StatusPermissionMixin

class StatusListView(ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'
    ordering = ['id']


class StatusCreateView(SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:index')
    success_message = 'Статус успешно создан'
    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class StatusUpdateView(StatusPermissionMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:index')
    success_message = 'Статус успешно изменен'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        return context


class StatusDeleteView(StatusPermissionMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:index')
    success_message = 'Статус успешно удален'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'delete'
        return context

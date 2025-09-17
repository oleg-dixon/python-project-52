from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView
)

from task_manager.mixins import (
    ContextActionMixin,
    DeleteProtectMixin,
    StatusPermissionMixin,
)

from .forms import StatusForm
from .models import Status


class StatusListView(ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'
    ordering = ['id']


class StatusCreateView(
    SuccessMessageMixin,
    ContextActionMixin,
    CreateView
):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Статус успешно создан')
    action = 'create'


class StatusUpdateView(
    SuccessMessageMixin,
    ContextActionMixin,
    UpdateView
):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Статус успешно изменен')
    action = 'update'


class StatusDeleteView(
    StatusPermissionMixin,
    DeleteProtectMixin,
    SuccessMessageMixin,
    ContextActionMixin,
    DeleteView
):
    model = Status
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:index')
    success_message = _('Статус успешно удален')
    redirect_url = reverse_lazy('statuses:index')
    protected_related_names = ['tasks']
    action = 'delete'

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView
)
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import (
    ContextActionMixin,
    DeleteProtectMixin,
    LabelPermissionMixin,
)

from .forms import LabelForm
from .models import Label


class LabelListView(ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'
    ordering = ['id']


class LabelCreateView(
    SuccessMessageMixin,
    ContextActionMixin,
    CreateView
):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels:index')
    success_message = _('Метка успешно создана')
    action = 'create'


class LabelUpdateView(
    SuccessMessageMixin,
    ContextActionMixin,
    UpdateView
):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels:index')
    success_message = _('Метка успешно изменена')
    action = 'update'


class LabelDeleteView(
    LabelPermissionMixin,
    DeleteProtectMixin,
    SuccessMessageMixin,
    ContextActionMixin,
    DeleteView
):
    model = Label
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels:index')
    success_message = _('Метка успешно удалена')
    redirect_url = reverse_lazy('labels:index')
    protected_related_names = ['tasks']
    action = 'delete'

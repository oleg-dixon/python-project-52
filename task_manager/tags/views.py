from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Tag
from .forms import TagForm
from task_manager.mixins import TagPermissionMixin, DeleteProtectMixin, ContextActionMixin


class TagListView(ListView):
    model = Tag
    template_name = 'tags/index.html'
    context_object_name = 'tags'
    ordering = ['id']


class TagCreateView(SuccessMessageMixin, ContextActionMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'tags/tag_form.html'
    success_url = reverse_lazy('tags:index')
    success_message = 'Метка успешно создана'
    action = 'create'


class TagUpdateView(TagPermissionMixin, SuccessMessageMixin, ContextActionMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'tags/tag_form.html'
    success_url = reverse_lazy('tags:index')
    success_message = 'Метка успешно изменена'
    action = 'update'


class TagDeleteView(TagPermissionMixin, DeleteProtectMixin, SuccessMessageMixin, ContextActionMixin, DeleteView):
    model = Tag
    template_name = 'tags/tag_form.html'
    success_url = reverse_lazy('tags:index')
    success_message = 'Метка успешно удалена'
    redirect_url = reverse_lazy('tags:index')
    protected_related_names = ['tasks']
    action = 'delete'

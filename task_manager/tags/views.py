from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Tag
from .forms import TagForm
from task_manager.mixins import TagPermissionMixin


class TagListView(ListView):
    model = Tag
    template_name = 'tags/index.html'
    context_object_name = 'tags'
    ordering = ['id']


class TagCreateView(SuccessMessageMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'tags/tag_form.html'
    success_url = reverse_lazy('tags:index')
    success_message = 'Метка успешно создана'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class TagUpdateView(TagPermissionMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'tags/tag_form.html'
    success_url = reverse_lazy('tags:index')
    success_message = 'Метка успешно изменена'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        return context


class TagDeleteView(TagPermissionMixin, DeleteView):
    model = Tag
    template_name = 'tags/tag_form.html'
    success_url = reverse_lazy('tags:index')
    success_message = 'Метка успешно удалена'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'delete'
        return context

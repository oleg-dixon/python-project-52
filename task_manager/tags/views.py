from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Tag
from .forms import TagForm


class TagListView(ListView):
    model = Tag
    template_name = 'tags/index.html'
    context_object_name = 'tags'
    ordering = ['id']


class TagCreateView(SuccessMessageMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'tags/create.html'
    success_url = reverse_lazy('tags:index')
    success_message = 'Метка успешно создана'


class TagUpdateView(SuccessMessageMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'tags/update.html'
    success_url = reverse_lazy('tags:index')
    success_message = 'Метка успешно изменена'


class TagDeleteView(SuccessMessageMixin, DeleteView):
    model = Tag
    template_name = 'tags/delete.html'
    success_url = reverse_lazy('tags:index')
    success_message = 'Метка успешно удалена'

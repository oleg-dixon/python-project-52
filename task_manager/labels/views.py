from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, View

from task_manager.mixins import LoginRequiredMixin

from .forms import LabelForm
from .models import Label


class LabelsView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'

    def get_queryset(self):
        return Label.objects.annotate().values(
            'id', 
            'name', 
            'time_create',
        ).order_by('time_create')


class CreateLabelView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = LabelForm()
        return render(request, 'labels/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно создана')
            return redirect('labels:labels')
        return render(request, 'labels/create.html', {'form': form})
    

class EditLabelView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/edit.html'
    success_url = reverse_lazy('labels:labels')

    def get_object(self, queryset=None):
        label = super().get_object(queryset)
        return label
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect(self.success_url)
        messages.success(request, 'Метка успешно изменена')
        return super().post(request, *args, **kwargs)
    

class DeleteLabelView(LoginRequiredMixin, View):
    success_url = reverse_lazy('labels:labels')
    template_name = 'labels/label_confirm_delete.html'

    def get_object(self):
        label_id = self.kwargs.get('pk')
        return get_object_or_404(Label, pk=label_id)

    def get(self, request, *args, **kwargs):
        label_to_delete = self.get_object()
        return render(request, self.template_name, {'label': label_to_delete})

    def post(self, request, *args, **kwargs):
        label_to_delete = self.get_object()
        try:
            label_to_delete.delete()
            messages.success(request, 'Метка успешно удалена')
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(
                request, 
                'Невозможно удалить метку, потому что она используется'
                )
            return redirect('labels:labels')
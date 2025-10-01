from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView, View

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

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Метка успешно изменена')
        return response
    

class DeleteLabelView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('labels:labels')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Метка успешно удалена')
            return response
        except ProtectedError:
            messages.error(
                self.request,
                'Невозможно удалить метку, потому что она используется'
            )
            return redirect(self.success_url)
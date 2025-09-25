from django.shortcuts import render
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    def get(self, request):
        return render(request, 'index.html')

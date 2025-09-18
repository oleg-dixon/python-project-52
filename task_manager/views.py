from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = _('Менеджер задач')
        return context

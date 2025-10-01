from django.contrib import messages
from django.shortcuts import redirect


class LoginRequiredMixin:  
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                'Вы не авторизованы! Пожалуйста, войдите в систему.'
            )
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)
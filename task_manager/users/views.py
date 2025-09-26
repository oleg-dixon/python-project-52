from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView
from django.db.models import Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View

from .forms import LoginUserForm, RegisterUserForm, UserEditForm

CustomUser = get_user_model()


class IndexView(ListView):
    model = CustomUser
    template_name = 'users/index.html'
    context_object_name = 'users'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                'Вы не авторизованы! Пожалуйста, войдите в систему.'
            )
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return CustomUser.objects.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).values(
            'id', 'username', 'full_name', 'date_joined'
        ).order_by('date_joined')


class RegistrationView(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Исправьте ошибки в форме')
        return super().form_invalid(form)


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Вы залогинены')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main_page')


class LogoutUserView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'Вы разлогинены')
            logout(request)
        return redirect('main_page')


class UserEditView(UpdateView):
    model = CustomUser
    form_class = UserEditForm
    template_name = 'users/edit.html'
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('users')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                'Вы не авторизованы! Пожалуйста, войдите в систему.'
            )
            return redirect('login')
        
        user_id = kwargs.get('user_id')
        if request.user.id != user_id:
            messages.error(
                request,
                'У вас нет прав для изменения другого пользователя.'
            )
            return redirect(self.success_url)
            
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно изменен')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Исправьте ошибки в форме')
        return super().form_invalid(form)


class UserDeleteView(View):
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                'Вы не авторизованы! Пожалуйста, войдите в систему.'
            )
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return get_object_or_404(CustomUser, pk=user_id)

    def get(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if request.user.id != user_to_delete.id:
            messages.error(request, 'У вас нет прав для удаления другого пользователя.')
            return redirect(self.success_url)
        return render(request, self.template_name, {'user': user_to_delete})

    def post(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if request.user.id != user_to_delete.id:
            messages.error(request, 'У вас нет прав для удаления другого пользователя.')
            return redirect(self.success_url)
        user_to_delete.delete()
        messages.success(request, 'Пользователь успешно удален')
        return redirect(self.success_url)
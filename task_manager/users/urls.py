from django.urls import path
from django.contrib.auth import views as auth_views
from task_manager.users.views import (
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    CustomLoginView,
)

app_name = 'users'

urlpatterns = [
    path("", UserListView.as_view(), name='index'),
    path('create/', UserCreateView.as_view(), name='create'),
    path('login/', CustomLoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='users:index'
    ), name='logout'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
]
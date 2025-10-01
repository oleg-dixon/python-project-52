from django.urls import path

from task_manager.users import views as user_views

app_name = 'users'

urlpatterns = [
     path('',
         user_views.UserView.as_view(),
         name='users'),
     path('create/',
         user_views.RegistrationView.as_view(),
         name='create_user'),
     path('login/',
         user_views.LoginUserView.as_view(),
         name='login'),
     path('logout/',
         user_views.LogoutUserView.as_view(),
         name='logout'),
     path('<int:pk>/update/',
         user_views.UserEditView.as_view(),
         name='edit_user'),
     path('<int:pk>/delete/',
         user_views.UserDeleteView.as_view(),
         name='delete_user'),
]

from django.urls import path

from task_manager.statuses import views as status_views

app_name = 'statuses'

urlpatterns = [
    path('',
         status_views.StatusView.as_view(),
         name='statuses'),
    path('create/',
         status_views.CreateStatusView.as_view(),
         name='create_status'),
    path('<int:pk>/update/',
         status_views.EditStatusView.as_view(),
         name='edit_status'),
    path('<int:pk>/delete/',
         status_views.StatusDeleteView.as_view(),
         name='delete_status'),
]

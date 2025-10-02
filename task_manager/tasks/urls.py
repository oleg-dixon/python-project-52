from django.urls import path

from task_manager.tasks import views as task_views

app_name = 'tasks'

urlpatterns = [
    path('',
         task_views.TaskView.as_view(),
         name='tasks'),
    path('<int:pk>/', 
        task_views.ShowTaskView.as_view(), 
        name='show_task'),
    path('create/',
         task_views.CreateTaskView.as_view(),
         name='create_task'),
    path('<int:pk>/update/',
         task_views.EditTaskView.as_view(),
         name='edit_task'),
    path('<int:pk>/delete/',
         task_views.DeleteTaskView.as_view(),
         name='delete_task'),
]

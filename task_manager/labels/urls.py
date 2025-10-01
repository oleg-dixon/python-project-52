from django.urls import path

from task_manager.labels import views as label_views

app_name = 'labels' 

urlpatterns = [
    path('',
         label_views.LabelsView.as_view(),
         name='labels'),
    path('create/',
         label_views.CreateLabelView.as_view(),
         name='create_label'),
    path('<int:pk>/update/',
         label_views.EditLabelView.as_view(),
         name='edit_label'),
    path('<int:pk>/delete/',
         label_views.DeleteLabelView.as_view(),
         name='delete_label'),
]

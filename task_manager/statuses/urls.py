from django.urls import path

from .views import (
    StatusCreateView,
    StatusDeleteView,
    StatusListView,
    StatusUpdateView,
)

app_name = 'statuses'

urlpatterns = [
    path('', StatusListView.as_view(), name='index'),
    path('create/', StatusCreateView.as_view(), name='create'),
    path('update/<int:pk>/', StatusUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', StatusDeleteView.as_view(), name='delete'),
]

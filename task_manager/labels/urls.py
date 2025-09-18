from django.urls import path

from .views import (
    LabelCreateView,
    LabelDeleteView,
    LabelListView,
    LabelUpdateView,
)

app_name = 'labels'

urlpatterns = [
    path('', LabelListView.as_view(), name='index'),
    path('create/', LabelCreateView.as_view(), name='create'),
    path('update/<int:pk>/', LabelUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', LabelDeleteView.as_view(), name='delete'),
]

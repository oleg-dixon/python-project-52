from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'status', 'author', 'executor', 'created_at', 'updated_at'
    )
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description', 'author__username', 'executor__username')
    list_filter = ('status', 'tags', 'author', 'executor')
    ordering = ('id',)
    filter_horizontal = ('tags',)

from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id',)

    def tasks_count(self, obj):
        return obj.tasks.count()

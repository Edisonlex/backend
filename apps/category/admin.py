from django.contrib import admin
from .models import Category
from unfold.admin import ModelAdmin
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'parent', 'display_thumbnail', 'display_children')
    list_filter = ('parent',)
    search_fields = ('name',)
    autocomplete_fields = ['parent']
    
    # Campos organizados en grupos
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'parent')
        }),
        ('Media', {
            'fields': ('thumbnail',),
            'classes': ('collapse',)
        }),
    )
    
    def display_thumbnail(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.get_thumbnail())
        return "No thumbnail"
    display_thumbnail.short_description = 'Thumbnail'
    
    def display_children(self, obj):
        children = obj.children.all()
        if children:
            return format_html(', '.join([f'<span style="background: #f0f0f0; padding: 2px 6px; border-radius: 4px; margin: 2px;">{child.name}</span>' for child in children]))
        return "No children"
    display_children.short_description = 'Child Categories'
    
    
from django.contrib import admin
from .models import Post
from unfold.admin import ModelAdmin
from django.utils.html import format_html

@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('title', 'status', 'category', 'published', 'display_thumbnail')
    list_filter = ('status', 'category', 'published')
    search_fields = ('title', 'description', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published'
    ordering = ('-published',)
    
    # Campos organizados en grupos
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'description', 'excerpt')
        }),
        ('Media', {
            'fields': ('thumbnail', 'video'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('category', 'status', 'published'),
            'classes': ('collapse',)
        }),
    )
    
    def display_thumbnail(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.get_thumbnail())
        return "No thumbnail"
    display_thumbnail.short_description = 'Thumbnail'

    # Personalización adicional
    save_on_top = True
    readonly_fields = ('blog_uuid',)
    list_per_page = 25
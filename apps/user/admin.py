from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from . import models

@admin.register(models.UserAccount)
class UserAccountAdmin(ModelAdmin):
    list_display = ('email', 'username', 'status_display', 'role_display')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    def status_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: #0f766e;">●</span> Active')
        return format_html('<span style="color: #dc2626;">●</span> Inactive')
    status_display.short_description = 'Status'

    def role_display(self, obj):
        if obj.is_superuser:
            return format_html('<span style="color: #4f46e5;">●</span> Superuser')
        elif obj.is_staff:
            return format_html('<span style="color: #0369a1;">●</span> Staff')
        return format_html('<span style="color: #737373;">●</span> User')
    role_display.short_description = 'Role'

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return self.fieldsets
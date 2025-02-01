from django.contrib import admin
from .models import Contact, Newsletter
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from django.utils.timesince import timesince

@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ('name', 'email', 'subject', 'phone', 'display_budget', 'time_since_contact')
    list_filter = ('contact_date', 'budget')
    search_fields = ('name', 'email', 'subject', 'message', 'phone')
    readonly_fields = ('contact_date',)
    date_hierarchy = 'contact_date'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'message', 'budget')
        }),
        ('Metadata', {
            'fields': ('contact_date',),
            'classes': ('collapse',)
        }),
    )

    def display_budget(self, obj):
        if obj.budget:
            return format_html('<span style="background: #e8f5e9; padding: 3px 10px; border-radius: 10px;">{}</span>', obj.budget)
        return format_html('<span style="color: #999;">No budget</span>')
    display_budget.short_description = 'Budget'

    def time_since_contact(self, obj):
        return format_html('<span title="{}">{} ago</span>', 
                         obj.contact_date.strftime('%Y-%m-%d %H:%M:%S'),
                         timesince(obj.contact_date))
    time_since_contact.short_description = 'Time Since Contact'

    # Personalización adicional
    save_on_top = True
    list_per_page = 25
    ordering = ('-contact_date',)


@admin.register(Newsletter)
class NewsletterAdmin(ModelAdmin):
    list_display = ('email', 'subscription_date', 'time_subscribed')
    list_filter = ('subscription_date',)
    search_fields = ('email',)
    readonly_fields = ('subscription_date',)
    date_hierarchy = 'subscription_date'
    
    fieldsets = (
        ('Subscription Information', {
            'fields': ('email', 'subscription_date')
        }),
    )

    def time_subscribed(self, obj):
        return format_html('<span title="{}">{} ago</span>', 
                         obj.subscription_date.strftime('%Y-%m-%d %H:%M:%S'),
                         timesince(obj.subscription_date))
    time_subscribed.short_description = 'Subscribed'

    # Personalización adicional
    save_on_top = True
    list_per_page = 50
    ordering = ('-subscription_date',)

    def has_change_permission(self, request, obj=None):
        # Solo permitir ver y eliminar suscriptores, no editar
        return False
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Contact, Newsletter

@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ('name', 'email', 'contact_date')
    search_fields = ('name', 'email')
    list_filter = ('contact_date',)

@admin.register(Newsletter)
class NewsletterAdmin(ModelAdmin):
    list_display = ('email', 'subscription_date')
    search_fields = ('email',)
    list_filter = ('subscription_date',)

class ContactoAppAdmin(admin.AdminSite):
    site_header = 'Contacto App'

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # Personaliza la lista de aplicaciones
        for app in app_list:
            if app['name'] == 'Contacto':
                app['models'] = [
                    {'name': 'Contacts', 'admin_url': '/admin/contacto/contact/'},
                    {'name': 'Newsletter', 'admin_url': '/admin/contacto/newsletter/'},
                ]
        return app_list

contacto_admin_site = ContactoAppAdmin(name='contacto_admin')
contacto_admin_site.register(Contact, ContactAdmin)
contacto_admin_site.register(Newsletter, NewsletterAdmin)
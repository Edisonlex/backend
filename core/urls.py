from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Rutas de la API
    path('api/user/', include('apps.user.urls')),
    path('api/blog/', include('apps.blog.urls')),
    path('api/category/', include('apps.category.urls')),
    path('api/contacts/', include('apps.contacts.urls')),
    path('api/courses/', include('apps.courses.urls')),

    # Admin y otras configuraciones
    path('admin/', admin.site.urls),
    
]
# Agregar esta línea para habilitar la carga de imágenes en el admin

# Rutas de React o frontend

if settings.DEBUG:
 urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""
URL configuration for app project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quotes/', include('quotes.urls')),
    path('', include('core.urls')),
]

# Serve media files in both development and production
urlpatterns += static(
    settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT,
)
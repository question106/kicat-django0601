"""
URL configuration for app project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os

# Debug view to test media file access
@csrf_exempt
def debug_media(request):
    media_root = settings.MEDIA_ROOT
    try:
        files = os.listdir(media_root)
        return HttpResponse(f"Media root: {media_root}<br>Files: {files}")
    except Exception as e:
        return HttpResponse(f"Error accessing media: {e}")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quotes/', include('quotes.urls')),
    path('', include('core.urls')),
    path('debug-media/', debug_media, name='debug_media'),
]

# Serve media files only in development (DEBUG=True)
# In production, nginx will serve media files directly
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT,
    )
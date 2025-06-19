"""
URL configuration for app project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap, QuoteRequestSitemap
import os

# Sitemap configuration
sitemaps = {
    'static': StaticViewSitemap,
    'quotes': QuoteRequestSitemap,
}

# Debug view to test media file access
@csrf_exempt
def debug_media(request):
    media_root = settings.MEDIA_ROOT
    try:
        files = os.listdir(media_root)
        return HttpResponse("Media root: {}<br>Files: {}".format(media_root, files))
    except Exception as e:
        return HttpResponse("Error accessing media: {}".format(e))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quotes/', include('quotes.urls')),
    path('', include('core.urls')),
    path('debug-media/', debug_media, name='debug_media'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Serve media files in both development and production
# This is needed because we're using nginx-proxy which forwards requests to Django
# Force media serving even in production (DEBUG=False)
from django.views.static import serve
from django.urls import re_path

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Force media serving in production
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

# Customize Django Admin Site Headers and Titles
admin.site.site_header = "KICAT Admin Dashboard"
admin.site.site_title = "KICAT Admin"
admin.site.index_title = "Welcome to KICAT Administration"
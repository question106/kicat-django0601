from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'weekly'
    protocol = 'https'
    
    def items(self):
        return [
            'core:home',
            'core:about', 
            'core:service_interpretation',
            'core:service_translation',
            'core:service_others',
            'core:cases',
            'core:korea_culture_arts_translation_agency',
        ]
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, obj):
        return timezone.now()


class QuoteRequestSitemap(Sitemap):
    """Sitemap for quote request page"""
    priority = 0.6
    changefreq = 'monthly'
    protocol = 'https'
    
    def items(self):
        return ['core:quote_request']
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, obj):
        return timezone.now() 
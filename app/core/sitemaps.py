from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    changefreq = 'weekly'
    protocol = 'https'
    
    # Priority mapping: homepage gets highest priority
    priority_map = {
        'core:home': 1.0,           # Homepage - highest priority
        'core:about': 0.8,
        'core:service_interpretation': 0.8,
        'core:service_translation': 0.8,
        'core:service_others': 0.7,
        'core:cases': 0.7,
        'core:korea_culture_arts_translation_agency': 0.6,
    }
    
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
    
    def priority(self, item):
        return self.priority_map.get(item, 0.5)
    
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
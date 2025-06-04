from django.views.generic import TemplateView
from quotes.models import Quote
from .models import Award
import math


class HomeView(TemplateView):
    template_name = 'core/home.html'
    http_method_names = ["get", "post"]
    model = Quote
    context_object_name = 'quotes'
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class AboutView(TemplateView):
    template_name = "core/about.html"
    http_method_names = ["get"]
    
class ServiceInterpretationView(TemplateView):
    template_name = "core/service-interpretation.html"
    http_method_names = ["get"]

class ServiceTranslationView(TemplateView):
    template_name = "core/service-translation.html"
    http_method_names = ["get"]
    
class ServiceOthersView(TemplateView):
    template_name = "core/service-others.html"
    http_method_names = ["get"]

class CasesView(TemplateView):
    template_name = "core/cases.html"
    http_method_names = ["get"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get active awards ordered by display_order and date
        awards = Award.objects.filter(is_active=True).order_by('display_order', '-date')
        
        # Group awards into slides (3 per slide)
        slides = []
        awards_list = list(awards)
        
        for i in range(0, len(awards_list), 3):
            slide_awards = awards_list[i:i+3]
            slides.append(slide_awards)
        
        context['awards'] = awards
        context['award_slides'] = slides
        context['total_slides'] = len(slides)
        
        return context

class KoreaCultureArtsTranslationAgencyView(TemplateView):
    template_name = "core/korea_culture_arts_translation_agency.html"
    http_method_names = ["get"]

class QuoteRequestView(TemplateView):
    template_name = "core/quote-request.html"
    http_method_names = ["get"]
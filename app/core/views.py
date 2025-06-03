from django.views.generic import TemplateView
from quotes.models import Quote


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

class KoreaCultureArtsTranslationAgencyView(TemplateView):
    template_name = "core/korea-culture-arts-translation-agency.html"
    http_method_names = ["get"]

class QuoteRequestView(TemplateView):
    template_name = "core/quote-request.html"
    http_method_names = ["get"]
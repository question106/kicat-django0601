from django.urls import path
from .views import (
    HomeView, AboutView, ServiceInterpretationView, 
    ServiceTranslationView, ServiceOthersView, CasesView,
    KoreaCultureArtsTranslationAgencyView, QuoteRequestView,
    robots_txt
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('service-interpretation', ServiceInterpretationView.as_view(), name='service_interpretation'),
    path('service-translation', ServiceTranslationView.as_view(), name='service_translation'),
    path('service-others', ServiceOthersView.as_view(), name='service_others'),
    path('cases', CasesView.as_view(), name='cases'),
    path('korea-culture-arts-translation-agency', KoreaCultureArtsTranslationAgencyView.as_view(), name='korea_culture_arts_translation_agency'),
    path('quote-request', QuoteRequestView.as_view(), name='quote_request'),
    path('robots.txt', robots_txt, name='robots_txt'),
] 
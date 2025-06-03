from django.urls import path
from .views import QuoteListView, CreateQuoteView, GetServiceTypesView, GenerateQuotePDFView

app_name = 'quotes'

urlpatterns = [
    path('', QuoteListView.as_view(), name='quote_list'),
    path('create/', CreateQuoteView.as_view(), name='create_quote'),
    path('get_service_types/', GetServiceTypesView.as_view(), name='get_service_types'),
    path('<int:quote_id>/generate_pdf/', GenerateQuotePDFView.as_view(), name='generate_pdf'),
]
from django.views.generic import ListView, CreateView, View
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import Quote, ServiceType, ServiceCategory
from .pdf_generator import generate_quote_pdf
import logging

logger = logging.getLogger(__name__)

class QuoteListView(ListView):
    http_method_names = ["get"]
    template_name = 'quotes/quote_list.html'
    model = Quote
    context_object_name = 'quotes'
    queryset = Quote.objects.all().order_by('-created_at')
    
class CreateQuoteView(CreateView):
    template_name = 'quotes/quote_request.html'
    http_method_names = ["get", "post"]
    model = Quote
    fields = ['name', 'company', 'email', 'phone', 'service_type', 'message', 'file', 'google_drive_link']
    success_url = "/"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_categories'] = ServiceCategory.objects.all()
        context['service_types'] = ServiceType.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            
            # Get service_type from POST data
            service_type_id = data.get('service_type')
            if not service_type_id:
                return JsonResponse({"status": "error", "message": "Service type is required"}, status=400)
            
            try:
                service_type = ServiceType.objects.get(id=service_type_id)
            except ServiceType.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Invalid service type"}, status=400)
            
            # Create the Quote object with correct fields
            quote = Quote(
                name=data.get('name', ''),
                company=data.get('company', ''),
                email=data.get('email', ''),
                phone=data.get('phone', ''),
                service_type=service_type,
                message=data.get('message', ''),
                google_drive_link=data.get('google_drive_link', '')
            )
            
            # Handle file if present
            if 'file' in request.FILES:
                quote.file = request.FILES['file']
                
            quote.full_clean()  # Validate the model
            quote.save()
            return JsonResponse({"status": "success"})
        except ValidationError as e:
            logger.error(f"Validation error creating quote: {e}")
            return JsonResponse({"status": "error", "message": "Invalid data provided"}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error creating quote: {e}")
            return JsonResponse({"status": "error", "message": "An error occurred. Please try again."}, status=500)

# Add this new view
class GetServiceTypesView(View):
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        if not category_id:
            return JsonResponse({
                'success': False,
                'service_types': []
            })
        
        try:
            service_types = ServiceType.objects.filter(
                category_id=category_id,
                is_active=True
            ).values('id', 'name')
            
            return JsonResponse({
                'success': True,
                'service_types': list(service_types)
            })
        except Exception as e:
            logger.error(f"Error fetching service types: {e}")
            return JsonResponse({
                'success': False,
                'service_types': []
            })

@method_decorator(staff_member_required, name='dispatch')
class GenerateQuotePDFView(View):
    """View to generate PDF quote for admin users"""
    
    def post(self, request, quote_id):
        try:
            quote = get_object_or_404(Quote, id=quote_id)
            
            # Generate PDF
            pdf_file = generate_quote_pdf(quote)
            
            # Save PDF to quote
            quote.prepared_quote_pdf.save(pdf_file.name, pdf_file, save=True)
            
            # Update status to quote_sent if needed
            if quote.status == 'prepare_quote':
                quote.status = 'quote_sent'
                quote.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Quote PDF generated successfully',
                'pdf_url': quote.prepared_quote_pdf.url if quote.prepared_quote_pdf else None
            })
            
        except Exception as e:
            logger.error(f"Error generating PDF for quote {quote_id}: {e}")
            return JsonResponse({
                'success': False,
                'message': f'Error generating PDF: {str(e)}'
            }, status=500)
    
    def get(self, request, quote_id):
        """Download the generated PDF"""
        try:
            quote = get_object_or_404(Quote, id=quote_id)
            
            if not quote.prepared_quote_pdf:
                return HttpResponse("No PDF available for this quote.", status=404)
            
            # Serve the PDF file
            response = HttpResponse(quote.prepared_quote_pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{quote.prepared_quote_pdf.name}"'
            return response
            
        except Exception as e:
            logger.error(f"Error downloading PDF for quote {quote_id}: {e}")
            return HttpResponse("Error downloading PDF.", status=500)
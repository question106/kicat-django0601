from django.views.generic import ListView, CreateView, View
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import Quote, ServiceType, ServiceCategory
from .pdf_generator import generate_quote_pdf
from email_service.services import (
    send_new_quote_notification_to_admin,
    send_quote_confirmation_to_customer,
    send_quote_ready_notification
)
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
            files = request.FILES
            
            # Debug logging
            logger.info("POST data: {}".format(data))
            logger.info("FILES data: {}".format(files))
            logger.info("Content length: {}".format(request.META.get('CONTENT_LENGTH', 'Not set')))
            
            # Get service_type from POST data
            service_type_id = data.get('service_type')
            if not service_type_id:
                logger.error("Service type not provided")
                return JsonResponse({"status": "error", "message": "Service type is required"}, status=400)
            
            try:
                service_type = ServiceType.objects.get(id=service_type_id)
            except ServiceType.DoesNotExist:
                logger.error("Service type {} does not exist".format(service_type_id))
                return JsonResponse({"status": "error", "message": "Invalid service type"}, status=400)
            
            # Check if file is required and present
            if 'file' not in files:
                logger.error("File is required but not present in request")
                return JsonResponse({"status": "error", "message": "File upload is required"}, status=400)
            
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
            
            # Handle file
            uploaded_file = files.get('file')
            if uploaded_file:
                logger.info("File uploaded: {}, size: {}".format(uploaded_file.name, uploaded_file.size))
                quote.file = uploaded_file
            else:
                logger.error("File upload field is empty")
                return JsonResponse({"status": "error", "message": "File upload is required"}, status=400)
                
            quote.full_clean()  # Validate the model
            quote.save()
            logger.info("Quote created successfully with ID: {}".format(quote.id))
            
            # Send email notifications
            send_new_quote_notification_to_admin(quote)
            #send_quote_confirmation_to_customer(quote)
            
            return JsonResponse({"status": "success"})
        except ValidationError as e:
            logger.error("Validation error creating quote: {}".format(e))
            error_messages = []
            if hasattr(e, 'error_dict'):
                for field, errors in e.error_dict.items():
                    for error in errors:
                        error_messages.append("{}: {}".format(field, error))
            else:
                error_messages = [str(e)]
            return JsonResponse({"status": "error", "message": "Validation failed: {}".format(', '.join(error_messages))}, status=400)
        except Exception as e:
            logger.error("Unexpected error creating quote: {}".format(e), exc_info=True)
            return JsonResponse({"status": "error", "message": "Server error: {}".format(str(e))}, status=500)

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
            logger.error("Error fetching service types: {}".format(e))
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
            
            # Send email notifications
            #send_quote_ready_notification(quote)
            
            return JsonResponse({
                'success': True,
                'message': 'Quote PDF generated successfully',
                'pdf_url': quote.prepared_quote_pdf.url if quote.prepared_quote_pdf else None
            })
            
        except Exception as e:
            logger.error("Error generating PDF for quote {}: {}".format(quote_id, e))
            return JsonResponse({
                'success': False,
                'message': 'Error generating PDF: {}'.format(str(e))
            }, status=500)
    
    def get(self, request, quote_id):
        """Download the generated PDF"""
        try:
            quote = get_object_or_404(Quote, id=quote_id)
            
            if not quote.prepared_quote_pdf:
                return HttpResponse("No PDF available for this quote.", status=404)
            
            # Serve the PDF file
            response = HttpResponse(quote.prepared_quote_pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(quote.prepared_quote_pdf.name)
            return response
            
        except Exception as e:
            logger.error("Error downloading PDF for quote {}: {}".format(quote_id, e))
            return HttpResponse("Error downloading PDF.", status=500)
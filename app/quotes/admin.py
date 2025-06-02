from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import redirect
from django.contrib import messages
from .models import ServiceCategory, ServiceType, QuoteStatus, Quote
from .pdf_generator import generate_quote_pdf


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'service_type', 'status', 'has_pdf', 'pdf_actions', 'created_at', 'updated_at')
    list_filter = ('service_type', 'status', 'created_at')
    search_fields = ('name', 'company', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'pdf_preview')
    
    fieldsets = (
        ('Client Information', {
            'fields': ('name', 'company', 'email', 'phone')
        }),
        ('Service Details', {
            'fields': ('service_type', 'message', 'file', 'google_drive_link')
        }),
        ('Quote Management', {
            'fields': ('status', 'prepared_quote_pdf', 'pdf_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['generate_pdf_quotes', 'mark_as_prepare_quote']
    
    def has_pdf(self, obj):
        """Check if quote has a generated PDF"""
        return bool(obj.prepared_quote_pdf)
    has_pdf.boolean = True
    has_pdf.short_description = 'PDF Generated'
    
    def pdf_actions(self, obj):
        """Show PDF action buttons"""
        html = ''
        
        # Generate PDF button
        generate_url = reverse('admin:generate_quote_pdf', args=[obj.pk])
        html += f'<a href="{generate_url}" class="button" style="margin-right: 5px;">Generate PDF</a>'
        
        # View/Download PDF button if PDF exists
        if obj.prepared_quote_pdf:
            pdf_url = reverse('quotes:generate_pdf', args=[obj.pk])
            html += f'<a href="{pdf_url}" class="button" target="_blank">View PDF</a>'
            
        return format_html(html)
    pdf_actions.short_description = 'PDF Actions'
    
    def pdf_preview(self, obj):
        """Show PDF preview link if PDF exists"""
        if obj.prepared_quote_pdf:
            pdf_url = reverse('quotes:generate_pdf', args=[obj.pk])
            return format_html(
                '<a href="{}" target="_blank">📄 View Generated PDF</a><br>'
                '<small>File: {}</small>',
                pdf_url,
                obj.prepared_quote_pdf.name
            )
        return "No PDF generated yet"
    pdf_preview.short_description = 'PDF Preview'
    
    def generate_pdf_quotes(self, request, queryset):
        """Admin action to generate PDFs for selected quotes"""
        count = 0
        for quote in queryset:
            try:
                pdf_file = generate_quote_pdf(quote)
                quote.prepared_quote_pdf.save(pdf_file.name, pdf_file, save=True)
                
                # Update status if it's 'prepare_quote'
                if quote.status == 'prepare_quote':
                    quote.status = 'quote_sent'
                    quote.save()
                    
                count += 1
            except Exception as e:
                messages.error(request, f"Error generating PDF for {quote.name}: {str(e)}")
                
        if count > 0:
            messages.success(request, f"Successfully generated {count} PDF quote(s)")
    generate_pdf_quotes.short_description = "Generate PDF quotes for selected items"
    
    def mark_as_prepare_quote(self, request, queryset):
        """Admin action to mark quotes as 'prepare_quote'"""
        updated = queryset.update(status='prepare_quote')
        messages.success(request, f"Marked {updated} quote(s) as 'Prepare Quote'")
    mark_as_prepare_quote.short_description = "Mark as 'Prepare Quote'"
    
    def get_urls(self):
        """Add custom URL for PDF generation"""
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:quote_id>/generate_pdf/',
                self.admin_site.admin_view(self.generate_pdf_view),
                name='generate_quote_pdf',
            ),
        ]
        return custom_urls + urls
    
    def generate_pdf_view(self, request, quote_id):
        """Custom admin view to generate PDF"""
        try:
            quote = Quote.objects.get(pk=quote_id)
            pdf_file = generate_quote_pdf(quote)
            quote.prepared_quote_pdf.save(pdf_file.name, pdf_file, save=True)
            
            # Update status if it's 'prepare_quote'
            if quote.status == 'prepare_quote':
                quote.status = 'quote_sent'
                quote.save()
                
            messages.success(request, f"PDF generated successfully for {quote.name}")
            
        except Quote.DoesNotExist:
            messages.error(request, "Quote not found")
        except Exception as e:
            messages.error(request, f"Error generating PDF: {str(e)}")
            
        return redirect('admin:quotes_quote_changelist')

class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name','category', 'description', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    
admin.site.register(Quote, QuoteAdmin)
admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
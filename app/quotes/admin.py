from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import redirect
from django.contrib import messages
from .models import ServiceCategory, ServiceType, QuoteStatus, Quote, QuoteItem
from .pdf_generator import generate_quote_pdf


class QuoteItemInline(admin.TabularInline):
    model = QuoteItem
    extra = 1
    fields = ('item_description', 'quantity', 'unit_price', 'formatted_total_price')
    readonly_fields = ('formatted_total_price',)
    
    def formatted_total_price(self, obj):
        """Format total price with Korean Won currency symbol for inline display"""
        if obj and obj.total_price:
            return "₩{:,.2f}".format(obj.total_price)
        return "₩0.00"
    formatted_total_price.short_description = 'Total Price'
    
    def get_readonly_fields(self, request, obj=None):
        """Make formatted_total_price read-only as it's auto-calculated"""
        return self.readonly_fields


class QuoteItemAdmin(admin.ModelAdmin):
    list_display = ('quote', 'item_description', 'quantity', 'formatted_unit_price', 'formatted_total_price', 'created_at')
    list_filter = ('quote__status', 'created_at', 'updated_at')
    search_fields = ('item_description', 'quote__name', 'quote__company')
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Item Details', {
            'fields': ('quote', 'item_description', 'quantity', 'unit_price', 'total_price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def formatted_unit_price(self, obj):
        """Format unit price with currency symbol"""
        return "₩{:,.2f}".format(obj.unit_price)
    formatted_unit_price.short_description = 'Unit Price'
    
    def formatted_total_price(self, obj):
        """Format total price with currency symbol"""
        return "₩{:,.2f}".format(obj.total_price)
    formatted_total_price.short_description = 'Total Price'


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'service_type', 'status', 'items_count', 'quote_total', 'has_pdf', 'pdf_actions', 'created_at', 'updated_at')
    list_filter = ('service_type', 'status', 'created_at')
    search_fields = ('name', 'company', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'pdf_preview', 'quote_summary')
    inlines = [QuoteItemInline]
    
    fieldsets = (
        ('Client Information', {
            'fields': ('name', 'company', 'email', 'phone')
        }),
        ('Service Details', {
            'fields': ('service_type', 'message', 'file', 'google_drive_link')
        }),
        ('Quote Summary', {
            'fields': ('quote_summary',),
            'classes': ('collapse',)
        }),
        ('Quote Management', {
            'fields': ('status', 'prepared_quote_pdf', 'pdf_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['generate_pdf_quotes', 'mark_as_prepare_quote']
    
    def items_count(self, obj):
        """Show number of quote items"""
        count = obj.items.count()
        if count > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">{} items</span>',
                count
            )
        else:
            return format_html(
                '<span style="color: orange;">No items</span>'
            )
    items_count.short_description = 'Items'
    
    def quote_total(self, obj):
        """Show total amount of the quote"""
        total = obj.total_amount
        if total > 0:
            formatted_total = "₩{:,.2f}".format(total)
            return format_html(
                '<span style="color: blue; font-weight: bold;">{}</span>',
                formatted_total
            )
        else:
            return format_html(
                '<span style="color: gray;">₩0.00</span>'
            )
    quote_total.short_description = 'Total Amount'
    
    def quote_summary(self, obj):
        """Show a summary of the quote with items and totals"""
        if obj.items.exists():
            items_html = ""
            for item in obj.items.all():
                items_html += """
                <tr>
                    <td>{}</td>
                    <td style="text-align: center;">{}</td>
                    <td style="text-align: right;">₩{:,.2f}</td>
                    <td style="text-align: right; font-weight: bold;">₩{:,.2f}</td>
                </tr>
                """.format(
                    item.item_description,
                    item.quantity,
                    item.unit_price,
                    item.total_price
                )
            
            summary_html = """
            <table style="width: 100%; border-collapse: collapse; margin: 10px 0;">
                <thead style="background-color: #f8f9fa;">
                    <tr>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Description</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: center;">Qty</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: right;">Unit Price</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: right;">Total</th>
                    </tr>
                </thead>
                <tbody>
                    {}
                </tbody>
                <tfoot style="background-color: #e9ecef; font-weight: bold;">
                    <tr>
                        <td colspan="3" style="border: 1px solid #ddd; padding: 8px; text-align: right;">Subtotal:</td>
                        <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">₩{:,.2f}</td>
                    </tr>
                    <tr>
                        <td colspan="3" style="border: 1px solid #ddd; padding: 8px; text-align: right;">Tax (10%):</td>
                        <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">₩{:,.2f}</td>
                    </tr>
                    <tr style="background-color: #710600; color: white;">
                        <td colspan="3" style="border: 1px solid #ddd; padding: 8px; text-align: right;">Total Amount:</td>
                        <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">₩{:,.2f}</td>
                    </tr>
                </tfoot>
            </table>
            """.format(
                items_html,
                obj.subtotal,
                obj.tax_amount,
                obj.total_amount
            )
            return format_html(summary_html)
        else:
            return format_html(
                '<p style="color: orange; font-style: italic;">No items added to this quote yet. Add items using the "Quote Items" section below.</p>'
            )
    quote_summary.short_description = 'Quote Summary'
    
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
        html += '<a href="{}" class="button" style="margin-right: 5px;">Generate PDF</a>'.format(generate_url)
        
        # View/Download PDF button if PDF exists
        if obj.prepared_quote_pdf:
            pdf_url = reverse('quotes:generate_pdf', args=[obj.pk])
            html += '<a href="{}" class="button" target="_blank">View PDF</a>'.format(pdf_url)
            
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
                messages.error(request, "Error generating PDF for {}: {}".format(quote.name, str(e)))
                
        if count > 0:
            messages.success(request, "Successfully generated {} PDF quote(s)".format(count))
    generate_pdf_quotes.short_description = "Generate PDF quotes for selected items"
    
    def mark_as_prepare_quote(self, request, queryset):
        """Admin action to mark quotes as 'prepare_quote'"""
        updated = queryset.update(status='prepare_quote')
        messages.success(request, "Marked {} quote(s) as 'Prepare Quote'".format(updated))
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
                
            messages.success(request, "PDF generated successfully for {}".format(quote.name))
            
        except Quote.DoesNotExist:
            messages.error(request, "Quote not found")
        except Exception as e:
            messages.error(request, "Error generating PDF: {}".format(str(e)))
            
        return redirect('admin:quotes_quote_changelist')

class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name','category', 'description', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    
admin.site.register(Quote, QuoteAdmin)
admin.site.register(QuoteItem, QuoteItemAdmin)
admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
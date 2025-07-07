from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import ServiceCategory, ServiceType, QuoteStatus, Quote, QuoteItem
from .pdf_generator import generate_quote_pdf


class QuoteItemInline(admin.TabularInline):
    model = QuoteItem
    extra = 1
    fields = ('item_description', 'quantity', 'unit_price', 'formatted_total_price')
    readonly_fields = ('formatted_total_price',)
    verbose_name = _("견적 항목")
    verbose_name_plural = _("견적 항목")
    
    def formatted_total_price(self, obj):
        """Format total price with Korean Won currency symbol for inline display"""
        if obj and obj.total_price:
            return "₩{:,.2f}".format(obj.total_price)
        return "₩0.00"
    formatted_total_price.short_description = _('총 금액')
    
    def get_readonly_fields(self, request, obj=None):
        """Make formatted_total_price read-only as it's auto-calculated"""
        return self.readonly_fields


class QuoteItemAdmin(admin.ModelAdmin):
    list_display = ('quote', 'item_description', 'quantity', 'formatted_unit_price', 'formatted_total_price', 'created_at')
    list_filter = ('quote__status', 'created_at', 'updated_at')
    search_fields = ('item_description', 'quote__name', 'quote__company')
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    
    fieldsets = (
        (_('항목 상세'), {
            'fields': ('quote', 'item_description', 'quantity', 'unit_price', 'total_price')
        }),
        (_('시간 정보'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def formatted_unit_price(self, obj):
        """Format unit price with currency symbol"""
        return "₩{:,.2f}".format(obj.unit_price)
    formatted_unit_price.short_description = _('단가')
    
    def formatted_total_price(self, obj):
        """Format total price with currency symbol"""
        return "₩{:,.2f}".format(obj.total_price)
    formatted_total_price.short_description = _('총 금액')


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'service_type', 'status', 'items_count', 'quote_total', 'has_pdf', 'pdf_actions', 'created_at', 'updated_at')
    list_filter = ('service_type', 'status', 'admin_notified', 'customer_notified', 'quote_sent_notified', 'created_at')
    search_fields = ('name', 'company', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'pdf_preview', 'quote_summary', 'last_notification_sent')
    inlines = [QuoteItemInline]
    
    fieldsets = (
        (_('고객 정보'), {
            'fields': ('name', 'company', 'email', 'phone')
        }),
        (_('서비스 상세'), {
            'fields': ('service_type', 'message', 'file', 'google_drive_link')
        }),
        (_('견적 요약'), {
            'fields': ('quote_summary',),
            'classes': ('collapse',)
        }),
        (_('견적 관리'), {
            'fields': ('status', 'prepared_quote_pdf', 'pdf_preview')
        }),
        # (_('이메일 알림 상태'), {
        #     'fields': ('admin_notified', 'customer_notified', 'quote_sent_notified', 'last_notification_sent'),
        #     'classes': ('collapse',)
        # }),
        (_('시간 정보'), {
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
                '<span style="color: green; font-weight: bold;">{} 개 항목</span>',
                count
            )
        else:
            return format_html(
                '<span style="color: orange;">항목 없음</span>'
            )
    items_count.short_description = _('항목 수')
    
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
    quote_total.short_description = _('총 금액')
    
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
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">설명</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: center;">수량</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: right;">단가</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: right;">총액</th>
                    </tr>
                </thead>
                <tbody>
                    {}
                </tbody>
                <tfoot style="background-color: #e9ecef; font-weight: bold;">
                    <tr>
                        <td colspan="3" style="border: 1px solid #ddd; padding: 8px; text-align: right;">소계:</td>
                        <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">₩{:,.2f}</td>
                    </tr>
                    <tr>
                        <td colspan="3" style="border: 1px solid #ddd; padding: 8px; text-align: right;">세금 (0%):</td>
                        <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">₩{:,.2f}</td>
                    </tr>
                    <tr style="background-color: #710600; color: white;">
                        <td colspan="3" style="border: 1px solid #ddd; padding: 8px; text-align: right;">총 금액:</td>
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
                '<p style="color: orange; font-style: italic;">이 견적서에 아직 항목이 추가되지 않았습니다. 아래 "견적 항목" 섹션을 사용하여 항목을 추가하세요.</p>'
            )
    quote_summary.short_description = _('견적 요약')
    
    def has_pdf(self, obj):
        """Check if quote has a generated PDF"""
        return bool(obj.prepared_quote_pdf)
    has_pdf.boolean = True
    has_pdf.short_description = _('PDF 생성됨')
    
    def email_status(self, obj):
        """Show email notification status"""
        admin_icon = '✅' if obj.admin_notified else '❌'
        customer_icon = '✅' if obj.customer_notified else '❌'
        quote_icon = '✅' if obj.quote_sent_notified else '❌'
        
        return format_html(
            '<div style="font-size: 11px; line-height: 1.2;">'
            '<div>관리자: {}</div>'
            '<div>고객확인: {}</div>'
            '<div>견적완료: {}</div>'
            '</div>',
            admin_icon,
            customer_icon,
            quote_icon
        )
    email_status.short_description = _('이메일 상태')
    
    def pdf_actions(self, obj):
        """Show PDF action buttons"""
        html = '<div style="display: flex; flex-direction: column; gap: 3px; min-width: 120px;">'
        
        # Generate PDF button
        generate_url = reverse('admin:generate_quote_pdf', args=[obj.pk])
        html += '<a href="{}" class="button" style="font-size: 11px; padding: 4px 8px; white-space: nowrap; text-align: center;">견적서 생성</a>'.format(generate_url)
        
        # View/Download PDF button if PDF exists
        if obj.prepared_quote_pdf:
            pdf_url = reverse('quotes:generate_pdf', args=[obj.pk])
            html += '<a href="{}" class="button" target="_blank" style="font-size: 11px; padding: 4px 8px; white-space: nowrap; text-align: center;">견적서 다운로드</a>'.format(pdf_url)
            
        html += '</div>'
        return format_html(html)
    pdf_actions.short_description = _('PDF 작업')
    
    def pdf_preview(self, obj):
        """Show PDF preview link if PDF exists"""
        if obj.prepared_quote_pdf:
            pdf_url = reverse('quotes:generate_pdf', args=[obj.pk])
            return format_html(
                '<a href="{}" target="_blank">📄 생성된 PDF 보기</a><br>'
                '<small>파일: {}</small>',
                pdf_url,
                obj.prepared_quote_pdf.name
            )
        return _("아직 PDF가 생성되지 않았습니다")
    pdf_preview.short_description = _('PDF 미리보기')
    
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
                messages.error(request, "{}의 PDF 생성 중 오류 발생: {}".format(quote.name, str(e)))
                
        if count > 0:
            messages.success(request, "{}개의 견적서 PDF가 성공적으로 생성되었습니다".format(count))
    generate_pdf_quotes.short_description = _("선택된 항목들의 견적서 PDF 생성")
    
    def mark_as_prepare_quote(self, request, queryset):
        """Admin action to mark quotes as 'prepare_quote'"""
        updated = queryset.update(status='prepare_quote')
        messages.success(request, "{}개의 견적서가 '견적서 준비' 상태로 변경되었습니다".format(updated))
    mark_as_prepare_quote.short_description = _("'견적서 준비' 상태로 변경")
    
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
                
            messages.success(request, "{}의 PDF가 성공적으로 생성되었습니다".format(quote.name))
            
        except Quote.DoesNotExist:
            messages.error(request, "견적서를 찾을 수 없습니다")
        except Exception as e:
            messages.error(request, "PDF 생성 중 오류 발생: {}".format(str(e)))
            
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
from django.db import models
from decimal import Decimal
from django.utils.translation import gettext_lazy as _

# Service Category
class ServiceCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("카테고리명"))
    description = models.TextField(null=True, blank=True, verbose_name=_("설명"))
    
    class Meta:
        verbose_name = _("서비스 카테고리")
        verbose_name_plural = _("서비스 카테고리")
    
    def __str__(self):
        return self.name

# Service Type
class ServiceType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("서비스명"))
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null=False, blank=False, verbose_name=_("카테고리"))
    description = models.TextField(null=True, blank=True, verbose_name=_("설명"))
    is_active = models.BooleanField(default=True, verbose_name=_("활성화"))
    
    class Meta:
        verbose_name = _("서비스 유형")
        verbose_name_plural = _("서비스 유형")
    
    def __str__(self):
        return self.name

# Quote Status
class QuoteStatus(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("상태명"))
    description = models.TextField(verbose_name=_("설명"))
    
    class Meta:
        verbose_name = _("견적 상태")
        verbose_name_plural = _("견적 상태")
    
    def __str__(self):
        return self.name

# Quote
class Quote(models.Model):
    STATUS_CHOICES = (
        ('pending', _('대기중')),
        ('prepare_quote', _('견적서 준비')),
        ('quote_sent', _('견적서 발송')),
        ('work_in_progress', _('작업중')),
        ('completed', _('완료')),
        ('cancelled', _('취소')),
    )
        
    name = models.CharField(max_length=255, verbose_name=_("고객명"))
    company = models.CharField(max_length=255, verbose_name=_("회사명"))
    email = models.EmailField(verbose_name=_("이메일"))
    phone = models.CharField(max_length=255, verbose_name=_("전화번호"))
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, verbose_name=_("서비스 유형"))
    message = models.TextField(verbose_name=_("메시지"))
    file = models.FileField(upload_to='quotes/', null=True, blank=True, verbose_name=_("첨부파일"))
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending', verbose_name=_("상태"))
    google_drive_link = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("구글 드라이브 링크"))
    prepared_quote_pdf = models.FileField(upload_to='prepared_quotes/', null=True, blank=True, 
                                        help_text=_("생성된 견적서 PDF"), verbose_name=_("견적서 PDF"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("생성일"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("수정일"))
    
    # Email notification tracking fields
    admin_notified = models.BooleanField(default=False, verbose_name=_("관리자 알림 전송됨"))
    customer_notified = models.BooleanField(default=False, verbose_name=_("고객 알림 전송됨"))
    quote_sent_notified = models.BooleanField(default=False, verbose_name=_("견적서 발송 알림됨"))
    last_notification_sent = models.DateTimeField(null=True, blank=True, verbose_name=_("마지막 알림 전송일"))

    class Meta:
        verbose_name = _("견적서")
        verbose_name_plural = _("견적서")
        ordering = ['-created_at']

    def __str__(self):
        return "{} - {}".format(self.name, self.company)
    
    @property
    def reference_number(self):
        """Generate a reference number based on ID and creation date"""
        if self.id:
            return f"QT-{self.created_at.strftime('%Y%m')}-{self.id:04d}"
        return "QT-PENDING"
    
    @property
    def subtotal(self):
        """Calculate subtotal from all quote items"""
        total = sum(item.total_price for item in self.items.all())
        return Decimal(str(total)) if total else Decimal('0.00')
    
    @property
    def tax_amount(self):
        """Tax amount (currently set to 0 - no automatic tax)"""
        return Decimal('0.00')
    
    @property
    def total_amount(self):
        """Calculate total amount (same as subtotal, no tax applied)"""
        return self.subtotal

# Quote Item
class QuoteItem(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='items', verbose_name=_("견적서"))
    item_description = models.CharField(max_length=500, help_text=_("서비스 또는 항목 설명"), verbose_name=_("항목 설명"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("수량"))
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text=_("원화 단위 가격"), verbose_name=_("단가"))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, help_text=_("총 가격 (수량 × 단가)"), verbose_name=_("총 금액"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("생성일"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("수정일"))
    
    class Meta:
        ordering = ['created_at']
        verbose_name = _("견적 항목")
        verbose_name_plural = _("견적 항목")
    
    def save(self, *args, **kwargs):
        """Automatically calculate total_price before saving"""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "{} (수량: {}) - ₩{:,.2f}".format(self.item_description, self.quantity, self.total_price)
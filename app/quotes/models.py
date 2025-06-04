from django.db import models
from decimal import Decimal

# Service Category
class ServiceCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

# Service Type
class ServiceType(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

# Quote Status
class QuoteStatus(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name

# Quote
class Quote(models.Model):
    STATUS_CHOICES = (
        ('pending', '대기중'),
        ('prepare_quote', 'Prepare Quote'),
        ('quote_sent', '견적서 발송'),
        ('work_in_progress', '작업중'),
        ('completed', '완료'),
        ('cancelled', '취소'),
    )
        
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    message = models.TextField()
    file = models.FileField(upload_to='quotes/', null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending')
    google_drive_link = models.CharField(max_length=255, null=True, blank=True)
    prepared_quote_pdf = models.FileField(upload_to='prepared_quotes/', null=True, blank=True, help_text="Generated PDF quote")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.company)
    
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
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='items')
    item_description = models.CharField(max_length=500, help_text="Description of the service or item")
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per unit in KRW")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total price (quantity × unit_price)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Quote Item"
        verbose_name_plural = "Quote Items"
    
    def save(self, *args, **kwargs):
        """Automatically calculate total_price before saving"""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "{} (Qty: {}) - ₩{:,.2f}".format(self.item_description, self.quantity, self.total_price)
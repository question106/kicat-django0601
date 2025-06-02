from django.db import models

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
        return f"{self.name} - {self.company}"
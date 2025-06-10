from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from django.db import transaction
import logging
import threading
from functools import wraps

logger = logging.getLogger(__name__)

def async_email(func):
    """Decorator to send emails asynchronously to avoid blocking the main thread"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        def run_async():
            try:
                func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Async email error: {e}")
        
        # Run in separate thread
        thread = threading.Thread(target=run_async)
        thread.daemon = True
        thread.start()
    return wrapper

@async_email
def send_new_quote_notification_to_admin(quote):
    """Send notification to admin when new quote is submitted"""
    try:
        # Check if already notified to prevent duplicates
        if quote.admin_notified:
            logger.info(f"Admin already notified for quote {quote.id}, skipping")
            return
            
        logger.info(f"Attempting to send admin notification for quote {quote.id}")
        logger.info(f"Email settings - Host: {settings.EMAIL_HOST}, Port: {settings.EMAIL_PORT}")
        logger.info(f"From: {settings.DEFAULT_FROM_EMAIL}, To: {settings.ADMIN_EMAIL}")
        
        subject = f'새로운 견적 요청 - {quote.name} ({quote.company})'
        
        # Create HTML content
        html_message = render_to_string('quotes/emails/new_quote_admin.html', {
            'quote': quote,
            'admin_url': f'{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else "localhost:8000"}/admin/quotes/quote/{quote.id}/'
        })
        
        # Create plain text version
        plain_message = strip_tags(html_message)
        
        logger.info("Email content prepared, attempting to send...")
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info("Email sent successfully!")
        
        # Update notification status atomically
        with transaction.atomic():
            quote.admin_notified = True
            quote.last_notification_sent = timezone.now()
            quote.save(update_fields=['admin_notified', 'last_notification_sent'])
            
        logger.info(f"Admin notification completed for quote {quote.id}")
        
    except Exception as e:
        logger.error(f"Failed to send admin notification for quote {quote.id}: {e}", exc_info=True)

@async_email
def send_quote_confirmation_to_customer(quote):
    """Send confirmation email to customer when quote is submitted"""
    try:
        # Check if already notified to prevent duplicates
        if quote.customer_notified:
            return
            
        subject = f'견적 요청 접수 확인 - {quote.company}'
        
        # Create HTML content
        html_message = render_to_string('quotes/emails/quote_confirmation_customer.html', {
            'quote': quote,
        })
        
        # Create plain text version
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[quote.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Update notification status atomically
        with transaction.atomic():
            quote.customer_notified = True
            quote.last_notification_sent = timezone.now()
            quote.save(update_fields=['customer_notified', 'last_notification_sent'])
            
        logger.info(f"Customer confirmation sent for quote {quote.id}")
        
    except Exception as e:
        logger.error(f"Failed to send customer confirmation for quote {quote.id}: {e}")

@async_email
def send_quote_ready_notification(quote):
    """Send notification to customer when quote PDF is ready"""
    try:
        # Check if already notified to prevent duplicates
        if quote.quote_sent_notified:
            return
            
        subject = f'견적서 준비 완료 - {quote.company}'
        
        # Create HTML content
        html_message = render_to_string('quotes/emails/quote_ready_customer.html', {
            'quote': quote,
        })
        
        # Create plain text version
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[quote.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Update notification status atomically
        with transaction.atomic():
            quote.quote_sent_notified = True
            quote.last_notification_sent = timezone.now()
            quote.save(update_fields=['quote_sent_notified', 'last_notification_sent'])
            
        logger.info(f"Quote ready notification sent for quote {quote.id}")
        
    except Exception as e:
        logger.error(f"Failed to send quote ready notification for quote {quote.id}: {e}")

def send_test_email():
    """Send a test email to verify email configuration"""
    try:
        send_mail(
            subject='KICAT 이메일 테스트',
            message='이메일 설정이 올바르게 구성되었습니다.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f"Test email failed: {e}")
        return False 
import logging
import threading
from functools import wraps
from mailjet_rest import Client
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

def async_email(func):
    """Decorator to send emails asynchronously to prevent blocking"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True  # Dies when main thread dies
        thread.start()
        logger.info(f"Started async email thread for {func.__name__}")
    return wrapper

class MailjetService:
    """Service class for handling Mailjet API operations"""
    
    def __init__(self):
        self.api_key = settings.MAILJET_API_KEY
        self.api_secret = settings.MAILJET_API_SECRET
        self.client = None
        
        if self.api_key and self.api_secret:
            self.client = Client(auth=(self.api_key, self.api_secret), version='v3.1')
        else:
            logger.warning("Mailjet credentials not configured")
    
    def send_email(self, to_email, to_name, subject, html_content, text_content=None, from_email=None, from_name=None):
        """
        Send email using Mailjet API
        
        Args:
            to_email: Recipient email address
            to_name: Recipient name
            subject: Email subject
            html_content: HTML email content
            text_content: Plain text content (optional, will be generated from HTML if not provided)
            from_email: Sender email (optional, uses DEFAULT_FROM_EMAIL if not provided)
            from_name: Sender name (optional, uses DEFAULT_FROM_EMAIL if not provided)
        
        Returns:
            dict: Response from Mailjet API
        """
        if not self.client:
            logger.error("Mailjet client not initialized - check API credentials")
            return {"success": False, "error": "Mailjet client not initialized"}
        
        # Parse default from email if needed
        if not from_email or not from_name:
            default_from = settings.DEFAULT_FROM_EMAIL
            if '<' in default_from and '>' in default_from:
                from_name = default_from.split('<')[0].strip()
                from_email = default_from.split('<')[1].replace('>', '').strip()
            else:
                from_email = default_from
                from_name = "KICAT System"
        
        # Generate text content if not provided
        if not text_content:
            text_content = strip_tags(html_content)
        
        # Prepare email data
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": from_email,
                        "Name": from_name
                    },
                    "To": [
                        {
                            "Email": to_email,
                            "Name": to_name
                        }
                    ],
                    "Subject": subject,
                    "TextPart": text_content,
                    "HTMLPart": html_content,
                    "CustomID": f"kicat-email-{hash(f'{to_email}-{subject}')}"
                }
            ]
        }
        
        try:
            # Send email via Mailjet API
            result = self.client.send.create(data=data)
            
            if result.status_code == 200:
                logger.info(f"Email sent successfully to {to_email}: {subject}")
                return {"success": True, "response": result.json()}
            else:
                logger.error(f"Failed to send email to {to_email}: {result.status_code} - {result.json()}")
                return {"success": False, "error": result.json()}
                
        except Exception as e:
            logger.error(f"Exception sending email to {to_email}: {str(e)}")
            return {"success": False, "error": str(e)}

# Initialize the service
mailjet_service = MailjetService()

@async_email
def send_new_quote_notification_to_admin(quote):
    """Send notification to all admin emails when a new quote request is submitted"""
    try:
        # Render HTML template
        html_content = render_to_string('email_service/admin_new_quote.html', {
            'quote': quote,
            'site_url': 'https://kicat.co.kr'
        })
        
        subject = f"[KICAT] 새로운 견적 요청 - {quote.service_type.category.name if quote.service_type and quote.service_type.category else '일반'}"
        
        # Send email to all admin addresses
        all_successful = True
        results = []
        
        for admin_email in settings.ADMIN_EMAILS:
            result = mailjet_service.send_email(
                to_email=admin_email,
                to_name="KICAT Admin",
                subject=subject,
                html_content=html_content
            )
            results.append(result)
            
            if result.get("success"):
                logger.info(f"Admin notification sent to {admin_email} for quote {quote.id}")
            else:
                logger.error(f"Failed to send admin notification to {admin_email} for quote {quote.id}: {result.get('error')}")
                all_successful = False
        
        # Update quote model if at least one email was sent successfully
        if any(result.get("success") for result in results):
            quote.admin_notified = True
            quote.save(update_fields=['admin_notified'])
            logger.info(f"Admin notification process completed for quote {quote.id}")
        else:
            logger.error(f"All admin notification attempts failed for quote {quote.id}")
            
    except Exception as e:
        logger.error(f"Exception in send_new_quote_notification_to_admin for quote {quote.id}: {str(e)}")

@async_email
def send_quote_confirmation_to_customer(quote):
    """Send confirmation email to customer after quote submission"""
    try:
        # Render HTML template
        html_content = render_to_string('email_service/customer_quote_confirmation.html', {
            'quote': quote,
            'site_url': 'https://kicat.co.kr'
        })
        
        # Send email
        result = mailjet_service.send_email(
            to_email=quote.email,
            to_name=quote.name,
            subject=f"[KICAT] 견적 요청이 접수되었습니다 - 참조번호: {quote.reference_number}",
            html_content=html_content
        )
        
        if result.get("success"):
            # Update quote model to mark customer as notified
            quote.customer_notified = True
            quote.save(update_fields=['customer_notified'])
            logger.info(f"Customer confirmation sent for quote {quote.id}")
        else:
            logger.error(f"Failed to send customer confirmation for quote {quote.id}: {result.get('error')}")
            
    except Exception as e:
        logger.error(f"Exception in send_quote_confirmation_to_customer for quote {quote.id}: {str(e)}")

@async_email
def send_quote_ready_notification(quote):
    """Send notification to customer when quote is ready"""
    try:
        # Render HTML template
        html_content = render_to_string('email_service/customer_quote_ready.html', {
            'quote': quote,
            'site_url': 'https://kicat.co.kr'
        })
        
        # Send email
        result = mailjet_service.send_email(
            to_email=quote.email,
            to_name=quote.name,
            subject=f"[KICAT] 견적서가 준비되었습니다 - 참조번호: {quote.reference_number}",
            html_content=html_content
        )
        
        if result.get("success"):
            # Update quote model to mark quote as sent
            quote.quote_sent_notified = True
            quote.save(update_fields=['quote_sent_notified'])
            logger.info(f"Quote ready notification sent for quote {quote.id}")
        else:
            logger.error(f"Failed to send quote ready notification for quote {quote.id}: {result.get('error')}")
            
    except Exception as e:
        logger.error(f"Exception in send_quote_ready_notification for quote {quote.id}: {str(e)}")

def send_test_email(to_email, to_name="Test User"):
    """Send a test email to verify Mailjet configuration"""
    try:
        html_content = """
        <html>
        <body>
            <h2>KICAT Mailjet Test Email</h2>
            <p>This is a test email to verify that Mailjet API is working correctly.</p>
            <p>If you receive this email, the configuration is successful!</p>
            <hr>
            <p><small>Sent via Mailjet API</small></p>
        </body>
        </html>
        """
        
        result = mailjet_service.send_email(
            to_email=to_email,
            to_name=to_name,
            subject="[KICAT] Mailjet Test Email",
            html_content=html_content
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Exception in send_test_email: {str(e)}")
        return {"success": False, "error": str(e)} 
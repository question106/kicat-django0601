from django.core.management.base import BaseCommand
from django.conf import settings
from email_service.services import mailjet_service
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import datetime


class Command(BaseCommand):
    help = 'Test admin notification email with sample quote data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to-email',
            type=str,
            help='Email address to send test admin notification to (default: ADMIN_EMAIL from settings)',
        )

    def handle(self, *args, **options):
        # Get recipient email
        to_email = options.get('to_email') or settings.ADMIN_EMAIL
        
        if not to_email:
            self.stdout.write(
                self.style.ERROR('No recipient email specified. Use --to-email or set ADMIN_EMAIL in settings.')
            )
            return
        
        # Check Mailjet credentials
        if not mailjet_service.client:
            self.stdout.write(
                self.style.ERROR('Mailjet client not initialized. Check MAILJET_API_KEY and MAILJET_API_SECRET.')
            )
            return
        
        self.stdout.write('Testing admin notification email...')
        self.stdout.write(f'Recipient: {to_email}')
        
        # Create sample quote data
        class MockQuote:
            def __init__(self):
                self.id = 123
                self.reference_number = "QT-2024-001"
                self.name = "김철수"
                self.email = "customer@example.com"
                self.phone = "010-1234-5678"
                self.company = "테스트 회사"
                self.source_language = "한국어"
                self.target_language = "영어"
                self.word_count = 500
                self.deadline = timezone.now().date()
                self.message = "이것은 테스트 견적 요청입니다."
                self.file = True  # Simulate file attachment
                self.created_at = timezone.now()
                self.service_category = MockServiceCategory()
        
        class MockServiceCategory:
            def __init__(self):
                self.name = "문서 번역"
        
        mock_quote = MockQuote()
        
        try:
            # Render HTML template
            html_content = render_to_string('email_service/admin_new_quote.html', {
                'quote': mock_quote,
                'site_url': 'https://kicat.co.kr'
            })
            
            # Send email
            result = mailjet_service.send_email(
                to_email=to_email,
                to_name="KICAT Admin",
                subject=f"[KICAT] 새로운 견적 요청 - {mock_quote.service_category.name}",
                html_content=html_content
            )
            
            if result.get("success"):
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Admin notification email sent successfully to {to_email}')
                )
                self.stdout.write(f'Response: {result.get("response", {})}')
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Failed to send admin notification email: {result.get("error")}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Exception sending admin notification: {str(e)}')
            )
            
        self.stdout.write('Test completed.') 
from django.core.management.base import BaseCommand
from django.conf import settings
from email_service.services import mailjet_service
from django.template.loader import render_to_string
from django.utils import timezone


class Command(BaseCommand):
    help = 'Test customer confirmation email with sample quote data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to-email',
            type=str,
            help='Email address to send test customer confirmation to',
            required=True
        )

    def handle(self, *args, **options):
        # Get recipient email
        to_email = options.get('to_email')
        
        # Check Mailjet credentials
        if not mailjet_service.client:
            self.stdout.write(
                self.style.ERROR('Mailjet client not initialized. Check MAILJET_API_KEY and MAILJET_API_SECRET.')
            )
            return
        
        self.stdout.write('Testing customer confirmation email...')
        self.stdout.write(f'Recipient: {to_email}')
        
        # Create sample quote data
        class MockQuote:
            def __init__(self):
                self.id = 123
                self.reference_number = "QT-2024-001"
                self.name = "김철수"
                self.email = to_email
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
            html_content = render_to_string('email_service/customer_quote_confirmation.html', {
                'quote': mock_quote,
                'site_url': 'https://kicat.co.kr'
            })
            
            # Send email
            result = mailjet_service.send_email(
                to_email=to_email,
                to_name=mock_quote.name,
                subject=f"[KICAT] 견적 요청이 접수되었습니다 - 참조번호: {mock_quote.reference_number}",
                html_content=html_content
            )
            
            if result.get("success"):
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Customer confirmation email sent successfully to {to_email}')
                )
                self.stdout.write(f'Response: {result.get("response", {})}')
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Failed to send customer confirmation email: {result.get("error")}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Exception sending customer confirmation: {str(e)}')
            )
            
        self.stdout.write('Test completed.') 
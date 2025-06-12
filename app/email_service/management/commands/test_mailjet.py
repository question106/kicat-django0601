from django.core.management.base import BaseCommand
from django.conf import settings
from email_service.services import send_test_email, mailjet_service


class Command(BaseCommand):
    help = 'Test Mailjet email functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to-email',
            type=str,
            help='Email address to send test email to (default: ADMIN_EMAIL from settings)',
        )
        parser.add_argument(
            '--to-name',
            type=str,
            default='Test User',
            help='Name of the recipient (default: Test User)',
        )

    def handle(self, *args, **options):
        # Get recipient email
        to_email = options.get('to_email') or settings.ADMIN_EMAIL
        to_name = options.get('to_name')
        
        if not to_email:
            self.stdout.write(
                self.style.ERROR('No recipient email specified. Use --to-email or set ADMIN_EMAILS in settings.')
            )
            return
        
        self.stdout.write('Testing Mailjet configuration...')
        self.stdout.write(f'Recipient: {to_name} <{to_email}>')
        
        # Check Mailjet credentials
        if not mailjet_service.client:
            self.stdout.write(
                self.style.ERROR('Mailjet client not initialized. Check MAILJET_API_KEY and MAILJET_API_SECRET.')
            )
            return
        
        self.stdout.write('✅ Mailjet credentials found')
        self.stdout.write(f'API Key: {settings.MAILJET_API_KEY[:8]}...')
        
        # Send test email
        self.stdout.write('Sending test email...')
        
        result = send_test_email(to_email, to_name)
        
        if result.get('success'):
            self.stdout.write(
                self.style.SUCCESS(f'✅ Test email sent successfully to {to_email}')
            )
            self.stdout.write(f'Response: {result.get("response", {})}')
        else:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to send test email: {result.get("error")}')
            )
            
        self.stdout.write('Test completed.') 
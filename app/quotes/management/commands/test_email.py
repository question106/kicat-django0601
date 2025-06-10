from django.core.management.base import BaseCommand
from django.conf import settings
from quotes.email_notifications import send_test_email
from quotes.models import Quote


class Command(BaseCommand):
    help = 'Test email functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['test', 'admin', 'customer', 'quote_ready'],
            default='test',
            help='Type of email to test'
        )
        parser.add_argument(
            '--quote-id',
            type=int,
            help='Quote ID for testing notifications'
        )

    def handle(self, *args, **options):
        email_type = options['type']
        
        if email_type == 'test':
            self.stdout.write('Testing basic email configuration...')
            success = send_test_email()
            if success:
                self.stdout.write(
                    self.style.SUCCESS(f'Test email sent successfully to {settings.ADMIN_EMAIL}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('Failed to send test email. Check email configuration.')
                )
        
        elif email_type in ['admin', 'customer', 'quote_ready']:
            quote_id = options.get('quote_id')
            if not quote_id:
                self.stdout.write(
                    self.style.ERROR('--quote-id is required for notification tests')
                )
                return
            
            try:
                quote = Quote.objects.get(id=quote_id)
            except Quote.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Quote with ID {quote_id} not found')
                )
                return
            
            if email_type == 'admin':
                from quotes.email_notifications import send_new_quote_notification_to_admin
                # Reset notification status for testing
                quote.admin_notified = False
                quote.save()
                send_new_quote_notification_to_admin(quote)
                self.stdout.write(
                    self.style.SUCCESS(f'Admin notification sent for quote {quote_id}')
                )
            
            elif email_type == 'customer':
                from quotes.email_notifications import send_quote_confirmation_to_customer
                # Reset notification status for testing
                quote.customer_notified = False
                quote.save()
                send_quote_confirmation_to_customer(quote)
                self.stdout.write(
                    self.style.SUCCESS(f'Customer confirmation sent for quote {quote_id}')
                )
            
            elif email_type == 'quote_ready':
                from quotes.email_notifications import send_quote_ready_notification
                # Reset notification status for testing
                quote.quote_sent_notified = False
                quote.save()
                send_quote_ready_notification(quote)
                self.stdout.write(
                    self.style.SUCCESS(f'Quote ready notification sent for quote {quote_id}')
                )
        
        self.stdout.write('\nEmail configuration:')
        self.stdout.write(f'EMAIL_HOST: {settings.EMAIL_HOST}')
        self.stdout.write(f'EMAIL_PORT: {settings.EMAIL_PORT}')
        self.stdout.write(f'EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}')
        self.stdout.write(f'EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}')
        self.stdout.write(f'DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'ADMIN_EMAIL: {settings.ADMIN_EMAIL}') 
from django.core.management.base import BaseCommand
from django.conf import settings
import smtplib
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Debug email configuration and test SMTP connection'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Email Configuration Debug Report'))
        self.stdout.write('=' * 60)
        
        # Check environment variables
        self.stdout.write('\n📧 Email Settings:')
        self.stdout.write(f'EMAIL_BACKEND: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'EMAIL_HOST: {settings.EMAIL_HOST}')
        self.stdout.write(f'EMAIL_PORT: {settings.EMAIL_PORT}')
        self.stdout.write(f'EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}')
        self.stdout.write(f'EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}')
        self.stdout.write(f'EMAIL_HOST_PASSWORD: {"***" + str(settings.EMAIL_HOST_PASSWORD)[-4:] if settings.EMAIL_HOST_PASSWORD else "NOT SET"}')
        self.stdout.write(f'DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'ADMIN_EMAIL: {settings.ADMIN_EMAIL}')
        self.stdout.write(f'DEBUG: {settings.DEBUG}')
        
        # Check for missing settings
        self.stdout.write('\n⚠️  Missing Settings Check:')
        missing = []
        if not settings.EMAIL_HOST_USER:
            missing.append('EMAIL_HOST_USER')
        if not settings.EMAIL_HOST_PASSWORD:
            missing.append('EMAIL_HOST_PASSWORD')
        
        if missing:
            self.stdout.write(self.style.ERROR(f'Missing: {", ".join(missing)}'))
        else:
            self.stdout.write(self.style.SUCCESS('All required settings present'))
        
        # Test SMTP connection
        self.stdout.write('\n🔌 SMTP Connection Test:')
        try:
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            self.stdout.write('✅ Connected to SMTP server')
            
            server.starttls()
            self.stdout.write('✅ TLS/SSL started successfully')
            
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                self.stdout.write('✅ Authentication successful')
            else:
                self.stdout.write('⚠️  No credentials provided for authentication')
            
            server.quit()
            self.stdout.write('✅ SMTP connection test passed')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ SMTP connection failed: {e}'))
            
        # Test Django send_mail
        self.stdout.write('\n📤 Django Email Test:')
        try:
            from django.core.mail import send_mail
            
            result = send_mail(
                subject='KICAT Production Email Test',
                message='This is a test email from the KICAT production server.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            if result:
                self.stdout.write(self.style.SUCCESS('✅ Django email test successful'))
            else:
                self.stdout.write(self.style.ERROR('❌ Django email test failed'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Django email test failed: {e}'))
        
        # Network connectivity test
        self.stdout.write('\n🌐 Network Connectivity Test:')
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((settings.EMAIL_HOST, settings.EMAIL_PORT))
            sock.close()
            
            if result == 0:
                self.stdout.write('✅ Network connection to SMTP server successful')
            else:
                self.stdout.write(self.style.ERROR(f'❌ Cannot reach {settings.EMAIL_HOST}:{settings.EMAIL_PORT}'))
                self.stdout.write('   Check firewall settings (outbound port 587 should be open)')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Network test failed: {e}'))
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('Debug complete! Check the results above for any issues.') 
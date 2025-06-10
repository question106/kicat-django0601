# Email Notification Setup Guide

## Overview

The email notification system has been implemented with the following features:

### 🔥 **Efficiency Improvements**
- **Asynchronous Email Sending**: Uses threading to prevent blocking the main application
- **Duplicate Prevention**: Tracks notification status to prevent duplicate emails
- **Atomic Database Updates**: Uses transactions to ensure data consistency
- **Error Handling**: Comprehensive logging and graceful error handling
- **Memory Efficient**: No heavy background task systems like Celery needed

### 📧 **Email Types**
1. **Admin Notification**: Sent when new quote is submitted
2. **Customer Confirmation**: Sent to customer when quote is received  
3. **Quote Ready**: Sent when PDF quote is prepared

## Email Configuration

### 1. Environment Variables

Update your `docker-compose.yml` or create a `.env` file with:

```env
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=kicat@kicat.co.kr
ADMIN_EMAIL=question106@gmail.com
```

### 2. Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account Settings → Security
   - Select "App passwords" 
   - Generate password for "Mail"
   - Use this password (not your regular Gmail password)

### 3. Alternative Email Providers

#### SendGrid (Production Recommended)
```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

#### Amazon SES
```env
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER=your-ses-smtp-username
EMAIL_HOST_PASSWORD=your-ses-smtp-password
```

## Testing Email Functionality

### 1. Basic Configuration Test
```bash
docker-compose exec app python manage.py test_email --type test
```

### 2. Test with Actual Quote
```bash
# First, find a quote ID
docker-compose exec app python manage.py shell -c "
from quotes.models import Quote
quotes = Quote.objects.all()[:5]
for q in quotes:
    print(f'ID: {q.id} - {q.name} ({q.company})')
"

# Test admin notification
docker-compose exec app python manage.py test_email --type admin --quote-id 1

# Test customer confirmation  
docker-compose exec app python manage.py test_email --type customer --quote-id 1

# Test quote ready notification
docker-compose exec app python manage.py test_email --type quote_ready --quote-id 1
```

## Development Mode (Console Backend)

For development/testing without real emails, you can use console backend:

In `app/app/settings.py`, modify the email backend:

```python
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

This will print emails to the console instead of sending them.

## Enabling Email Notifications

Currently, some notifications are commented out in `app/quotes/views.py`. To enable them:

### 1. Customer Confirmation (on quote submission)
```python
# In CreateQuoteView.post method
send_new_quote_notification_to_admin(quote)
send_quote_confirmation_to_customer(quote)  # Uncomment this line
```

### 2. Quote Ready Notification (when PDF is generated)
```python
# In GenerateQuotePDFView.post method  
send_quote_ready_notification(quote)  # Uncomment this line
```

## Admin Interface Features

The admin interface now shows:
- **Email Status Column**: Shows which notifications have been sent
- **Email Filters**: Filter quotes by notification status
- **Email Fields**: View/edit notification tracking fields

## Database Fields Added

The Quote model now includes:
- `admin_notified`: Boolean - Admin notification sent
- `customer_notified`: Boolean - Customer confirmation sent  
- `quote_sent_notified`: Boolean - Quote ready notification sent
- `last_notification_sent`: DateTime - Last notification timestamp

## Troubleshooting

### Common Issues

1. **Authentication Error (530)**
   - Check email credentials
   - Use app-specific password for Gmail
   - Verify 2FA is enabled

2. **Connection Timeout**
   - Check EMAIL_HOST and EMAIL_PORT
   - Verify firewall/network settings
   - Try different port (465 for SSL)

3. **SSL/TLS Errors**
   - For port 465: Set `EMAIL_USE_SSL=1` instead of `EMAIL_USE_TLS`
   - For port 587: Use `EMAIL_USE_TLS=1`

### Debug Commands

```bash
# Check email settings
docker-compose exec app python manage.py shell -c "
from django.conf import settings
print('EMAIL_HOST:', settings.EMAIL_HOST)
print('EMAIL_PORT:', settings.EMAIL_PORT)
print('EMAIL_USE_TLS:', settings.EMAIL_USE_TLS)
print('EMAIL_HOST_USER:', settings.EMAIL_HOST_USER)
print('DEFAULT_FROM_EMAIL:', settings.DEFAULT_FROM_EMAIL)
"

# Test SMTP connection
docker-compose exec app python manage.py shell -c "
import smtplib
from django.conf import settings
try:
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.starttls()
    print('SMTP connection successful')
    server.quit()
except Exception as e:
    print('SMTP connection failed:', e)
"
```

## Production Deployment

1. **Use Environment Variables**: Never hardcode credentials
2. **Use Professional Email Service**: SendGrid, Amazon SES, etc.
3. **Monitor Email Delivery**: Set up bounce/complaint handling
4. **Rate Limiting**: Consider implementing rate limits for email sending
5. **Email Templates**: Test templates across different email clients

## Performance Notes

This implementation is designed to be lightweight and efficient:
- **No Celery Required**: Uses simple threading for async email sending
- **Database Efficient**: Minimal additional fields and optimized queries  
- **Memory Friendly**: Small memory footprint compared to task queue systems
- **Fast Response**: Non-blocking email sending keeps UI responsive

The threading approach is suitable for moderate email volumes. For high-volume applications, consider implementing Celery or Redis-based task queues. 
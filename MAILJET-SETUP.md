# Mailjet Email Service Setup Guide

## Overview
This project now uses Mailjet API for email delivery instead of SMTP, which bypasses the SMTP port restrictions that were blocking email delivery on Digital Ocean.

## Features
- HTTP-based email delivery (bypasses SMTP port blocks)
- Async email sending to prevent blocking the main application
- Professional HTML email templates
- Email delivery tracking and logging
- Fallback to console backend in development

## Setup Instructions

### 1. Create Mailjet Account
1. Go to [Mailjet.com](https://www.mailjet.com)
2. Sign up for a free account
3. Verify your account and domain

### 2. Get API Credentials
1. Login to Mailjet dashboard
2. Go to Account Settings → API Keys
3. Copy your API Key and Secret Key

### 3. Configure Environment Variables

#### For Local Development
Create a `.env` file (or set environment variables):
```bash
MAILJET_API_KEY=your_mailjet_api_key_here
MAILJET_API_SECRET=your_mailjet_api_secret_here
DEFAULT_FROM_EMAIL=KICAT System <wowkjobs@gmail.com>
ADMIN_EMAIL=question106@gmail.com
```

#### For Production (Digital Ocean + Portainer)
1. Go to Portainer dashboard
2. Navigate to Stacks → kicat-production
3. Click "Environment variables"
4. Add the following variables:
   - `MAILJET_API_KEY`: Your Mailjet API key
   - `MAILJET_API_SECRET`: Your Mailjet API secret
   - `DEFAULT_FROM_EMAIL`: KICAT System <wowkjobs@gmail.com>
   - `ADMIN_EMAIL`: question106@gmail.com

### 4. Verify Sender Domain
1. In Mailjet dashboard, go to Account Settings → Sender Domains
2. Add and verify your domain (e.g., `kicat.co.kr`)
3. Follow DNS verification steps

## Testing

### Test Email Service
Run this command in the Django container:
```bash
docker exec -it kicat-django0601-app-1 python manage.py test_mailjet --to-email your@email.com
```

### Check Email Service Status
```bash
docker exec -it kicat-django0601-app-1 python manage.py shell
```
Then in the shell:
```python
from email_service.services import mailjet_service
print("Client initialized:", mailjet_service.client is not None)
```

## Email Templates
The service includes three professional HTML email templates:
1. **Admin Notification**: When new quotes are submitted
2. **Customer Confirmation**: When quote requests are received
3. **Quote Ready**: When quotes are prepared and ready

## Architecture
- **email_service** app: Dedicated Django app for email functionality
- **services.py**: Mailjet API integration and email functions
- **templates/**: Professional HTML email templates
- **management/commands/**: Testing and debugging commands

## Troubleshooting

### No emails being received
1. Check Mailjet dashboard for delivery logs
2. Verify API credentials are set correctly
3. Check Django logs for error messages
4. Ensure sender domain is verified in Mailjet

### API Key Issues
1. Make sure API key has sending permissions
2. Check if API key is active (not expired)
3. Verify secret key matches in Mailjet dashboard

### Template Errors
1. Check Django logs for template rendering errors
2. Verify all required context variables are available
3. Test with simple text email first

## Deployment

### Local Development
```bash
docker-compose up --build
```

### Production Deployment
1. Update environment variables in Portainer
2. Restart the stack
3. Test email functionality

## Benefits Over SMTP
- ✅ Bypasses SMTP port restrictions (587, 465)
- ✅ Better delivery rates and reputation management
- ✅ Detailed delivery analytics and tracking
- ✅ Automatic bounce and spam handling
- ✅ API-based (more reliable than SMTP)
- ✅ Free tier: 200 emails/day, 6,000/month 
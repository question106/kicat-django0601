#!/usr/bin/env python3
"""
Generate a new Django secret key for production deployment
"""

try:
    from django.core.management.utils import get_random_secret_key
    
    secret_key = get_random_secret_key()
    print("🔑 Generated Django Secret Key:")
    print(f"SECRET_KEY={secret_key}")
    print()
    print("💡 Copy this key and use it in your Portainer environment variables")
    print("⚠️  Keep this key secure and never commit it to version control!")
    
except ImportError:
    import secrets
    import string
    
    # Generate a 50-character secret key
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    secret_key = ''.join(secrets.choice(alphabet) for i in range(50))
    
    print("🔑 Generated Django Secret Key:")
    print(f"SECRET_KEY={secret_key}")
    print()
    print("💡 Copy this key and use it in your Portainer environment variables")
    print("⚠️  Keep this key secure and never commit it to version control!") 
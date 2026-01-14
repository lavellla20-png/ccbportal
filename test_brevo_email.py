#!/usr/bin/env python
"""
Test BREVO email sending directly
Run this to verify BREVO API key is working
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ccb_portal_backend.settings')
django.setup()

from django.conf import settings
from anymail.message import AnymailMessage

print("="*60)
print("Testing BREVO Email Configuration")
print("="*60)

# Check BREVO_API_KEY
brevo_key = getattr(settings, 'BREVO_API_KEY', None)
if not brevo_key:
    print("[ERROR] BREVO_API_KEY is not set in Django settings")
    sys.exit(1)

print(f"[OK] BREVO_API_KEY is set (length: {len(brevo_key)})")
print(f"[OK] EMAIL_BACKEND: {getattr(settings, 'EMAIL_BACKEND', 'NOT SET')}")
print(f"[OK] DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'NOT SET')}")

# Test creating an AnymailMessage
try:
    test_email = input("\nEnter a test email address (or press Enter to skip sending): ").strip()
    
    if test_email:
        print(f"\n[SENDING] Sending test email to {test_email}...")
        msg = AnymailMessage(
            subject="Test Email from CCB Portal",
            body="<p>This is a test email from City College of Bayawan Portal.</p><p>If you receive this, BREVO API is working correctly!</p>",
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'citycollegeofbayawan@gmail.com'),
            to=[test_email],
        )
        msg.content_subtype = 'html'
        msg.send(fail_silently=False)
        print("[SUCCESS] Test email sent successfully!")
        print("Check your inbox (and spam folder) for the test email.")
    else:
        print("\n[SKIPPED] Email sending test skipped.")
        print("[INFO] AnymailMessage can be created successfully.")
        
except Exception as e:
    print(f"\n[ERROR] Failed to send test email: {e}")
    print("\nPossible issues:")
    print("1. BREVO API key might be invalid")
    print("2. Sender email (citycollegeofbayawan@gmail.com) might not be verified in BREVO")
    print("3. BREVO account might have sending limits")
    print("\nCheck BREVO dashboard: https://app.brevo.com/")
    sys.exit(1)

print("\n" + "="*60)
print("Test completed!")
print("="*60)


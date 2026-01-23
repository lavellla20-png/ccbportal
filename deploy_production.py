#!/usr/bin/env python3
"""
Production deployment script for CCB Portal
This script helps configure the application for production deployment on Render
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        'PUBLIC_BASE_URL',
        'CORS_ALLOWED_ORIGINS',
        'REACT_APP_API_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these in your Render dashboard or .env file")
        return False
    
    print("✅ All required environment variables are set")
    return True

def check_django_settings():
    """Check Django settings for production"""
    try:
        # Import Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ccb_portal_backend.settings')
        import django
        django.setup()
        from django.conf import settings
        
        print(f"DEBUG mode: {settings.DEBUG}")
        print(f"Allowed hosts: {settings.ALLOWED_HOSTS}")
        print(f"CORS allowed origins: {getattr(settings, 'CORS_ALLOWED_ORIGINS', 'Not set')}")
        
        # Check if we're in production mode
        if settings.DEBUG:
            print("⚠️  WARNING: DEBUG mode is enabled. This should be disabled in production.")
        else:
            print("✅ DEBUG mode is disabled")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking Django settings: {e}")
        return False

def check_media_configuration():
    """Check media file configuration"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ccb_portal_backend.settings')
        import django
        django.setup()
        from django.conf import settings
        
        print(f"Media URL: {settings.MEDIA_URL}")
        print(f"Media root: {settings.MEDIA_ROOT}")
        
        # Check if media directory exists
        media_root = Path(settings.MEDIA_ROOT)
        if not media_root.exists():
            print(f"⚠️  Media directory does not exist: {media_root}")
            print("Creating media directory...")
            media_root.mkdir(parents=True, exist_ok=True)
            print("✅ Media directory created")
        else:
            print("✅ Media directory exists")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking media configuration: {e}")
        return False

def run_migrations():
    """Run Django migrations"""
    try:
        print("Running Django migrations...")
        result = subprocess.run([
            sys.executable, 'manage.py', 'migrate'
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Migrations completed successfully")
            return True
        else:
            print(f"❌ Migration failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        return False

def collect_static():
    """Collect static files"""
    try:
        print("Collecting static files...")
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput'
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Static files collected successfully")
            return True
        else:
            print(f"❌ Static collection failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error collecting static files: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 CCB Portal Production Deployment Check")
    print("=" * 50)
    
    # Check environment variables
    if not check_environment():
        return False
    
    print("\n" + "=" * 50)
    
    # Check Django settings
    if not check_django_settings():
        return False
    
    print("\n" + "=" * 50)
    
    # Check media configuration
    if not check_media_configuration():
        return False
    
    print("\n" + "=" * 50)
    
    # Run migrations
    if not run_migrations():
        return False
    
    print("\n" + "=" * 50)
    
    # Collect static files
    if not collect_static():
        return False
    
    print("\n" + "=" * 50)
    print("✅ Production deployment check completed successfully!")
    print("\nNext steps:")
    print("1. Ensure your Render backend service is configured with the correct environment variables")
    print("2. Ensure your Render frontend service has REACT_APP_API_URL set to your backend URL")
    print("3. Test image upload and display functionality")
    print("4. Monitor the application logs for any issues")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
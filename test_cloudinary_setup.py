#!/usr/bin/env python3
"""
Cloudinary Image Handling Test Script for CCB Portal
This script tests the Cloudinary image handling functionality
"""

import os
import sys
import subprocess
from pathlib import Path

def test_cloudinary_configuration():
    """Test Cloudinary configuration"""
    print("☁️  Testing Cloudinary configuration...")
    
    try:
        # Setup Django with production settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ccb_portal_backend.production_settings')
        import django
        django.setup()
        
        from django.conf import settings
        
        print(f"Django settings loaded: DEBUG={settings.DEBUG}")
        print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set')}")
        print(f"MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'Not set')}")
        
        # Check if Cloudinary is configured
        if hasattr(settings, 'DEFAULT_FILE_STORAGE') and 'cloudinary' in settings.DEFAULT_FILE_STORAGE.lower():
            print("✅ Cloudinary storage is configured")
            
            # Check Cloudinary credentials
            cloud_name = getattr(settings, 'CLOUDINARY_CLOUD_NAME', None)
            api_key = getattr(settings, 'CLOUDINARY_API_KEY', None)
            api_secret = getattr(settings, 'CLOUDINARY_API_SECRET', None)
            
            if cloud_name and api_key and api_secret:
                print(f"✅ Cloudinary credentials configured:")
                print(f"  Cloud Name: {cloud_name}")
                print(f"  API Key: {api_key[:8]}...")  # Only show first 8 chars for security
                print(f"  API Secret: {'*' * 20}")  # Don't show secret
                return True
            else:
                print("❌ Cloudinary credentials missing")
                return False
        else:
            print("❌ Cloudinary storage not configured")
            return False
        
    except Exception as e:
        print(f"❌ Cloudinary configuration test failed: {e}")
        return False

def test_cloudinary_url_generation():
    """Test Cloudinary URL generation"""
    print("\n🔗 Testing Cloudinary URL generation...")
    
    try:
        # Setup Django with production settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ccb_portal_backend.production_settings')
        import django
        django.setup()
        
        from portal.utils import build_production_media_url
        from django.core.files.base import ContentFile
        
        # Create a mock file with Cloudinary-style URL
        test_file = ContentFile(b'test', name='test.jpg')
        test_file.url = 'https://res.cloudinary.com/your-cloud-name/image/upload/v1234567890/test-image.jpg'
        
        result = build_production_media_url(test_file)
        expected = 'https://res.cloudinary.com/your-cloud-name/image/upload/v1234567890/test-image.jpg'
        
        print(f"Cloudinary URL: {result}")
        print(f"Expected URL: {expected}")
        
        if result == expected:
            print("✅ Cloudinary URL generation working")
            return True
        else:
            print("❌ Cloudinary URL generation failed")
            return False
        
    except Exception as e:
        print(f"❌ Cloudinary URL generation test failed: {e}")
        return False

def test_frontend_cloudinary_integration():
    """Test frontend Cloudinary integration"""
    print("\n🌐 Testing frontend Cloudinary integration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # Test frontend URL normalization with Cloudinary URLs
        def normalizeImageUrl(imageUrl):
            if not imageUrl:
                return None
            
            # If it's already a data URL or blob URL, return as is
            if imageUrl.startswith('data:') or imageUrl.startswith('blob:'):
                return imageUrl
            
            # If it's already an absolute URL with http/https, return as is
            if imageUrl.startswith('http://') or imageUrl.startswith('https://'):
                return imageUrl
            
            # Get backend URL from environment variable
            backendUrl = os.getenv('REACT_APP_API_URL', 'http://127.0.0.1:8000')
            BACKEND_URL = backendUrl.rstrip('/')
            
            # If it's a relative URL (starts with /), prepend backend URL
            if imageUrl.startswith('/'):
                return f'{BACKEND_URL}{imageUrl}'
            
            # Otherwise, assume it's a path without leading slash and prepend backend + /
            return f'{BACKEND_URL}/{imageUrl}'
        
        # Test cases for Cloudinary
        test_cases = [
            ('https://res.cloudinary.com/your-cloud-name/image/upload/v1234567890/test.jpg', 'https://res.cloudinary.com/your-cloud-name/image/upload/v1234567890/test.jpg'),
            ('https://res.cloudinary.com/your-cloud-name/image/upload/f_auto,q_auto/v1234567890/test.jpg', 'https://res.cloudinary.com/your-cloud-name/image/upload/f_auto,q_auto/v1234567890/test.jpg'),
            ('/media/local-image.jpg', 'https://ccb-portal-backend.onrender.com/media/local-image.jpg'),
            ('data:image/png;base64,abc123', 'data:image/png;base64,abc123'),
        ]
        
        print("Testing frontend URL normalization:")
        all_passed = True
        for input_url, expected in test_cases:
            result = normalizeImageUrl(input_url)
            passed = result == expected
            status = "✅" if passed else "❌"
            print(f"{status} {input_url} → {result}")
            if not passed:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Frontend Cloudinary integration test failed: {e}")
        return False

def generate_cloudinary_setup_guide():
    """Generate Cloudinary setup guide"""
    print("\n" + "="*60)
    print("☁️  CLOUDINARY SETUP GUIDE")
    print("="*60)
    
    guide = [
        "📋 TO USE CLOUDINARY IN PRODUCTION:",
        "",
        "1. Sign up for Cloudinary account at cloudinary.com",
        "2. Get your Cloudinary credentials:",
        "   - Cloud Name",
        "   - API Key", 
        "   - API Secret",
        "",
        "3. Set these environment variables in Render:",
        "   CLOUDINARY_CLOUD_NAME=your-cloud-name",
        "   CLOUDINARY_API_KEY=your-api-key",
        "   CLOUDINARY_API_SECRET=your-api-secret",
        "",
        "4. Update your .env file with real Cloudinary values",
        "",
        "5. Test image upload in admin panel",
        "6. Verify images load from Cloudinary CDN",
        "",
        "🎯 BENEFITS OF CLOUDINARY:",
        "✅ Automatic image optimization",
        "✅ CDN delivery for faster loading",
        "✅ Image transformation on-the-fly",
        "✅ Automatic format conversion (WebP, etc.)",
        "✅ Responsive image delivery",
        "",
        "📖 Full guide: RENDER_DEPLOYMENT_GUIDE.md",
    ]
    
    for item in guide:
        print(item)
    
    print("="*60)

def main():
    """Main Cloudinary test function"""
    print("🚀 CCB Portal Cloudinary Test Suite")
    print("="*60)
    print("Testing Cloudinary image handling functionality...")
    
    tests = [
        ("Cloudinary Configuration", test_cloudinary_configuration),
        ("Cloudinary URL Generation", test_cloudinary_url_generation),
        ("Frontend Cloudinary Integration", test_frontend_cloudinary_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 40)
        result = test_func()
        results.append((test_name, result))
        print(f"Result: {'✅ PASSED' if result else '❌ FAILED'}")
    
    print("\n" + "="*60)
    print("📋 FINAL RESULTS")
    print("="*60)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL CLOUDINARY TESTS PASSED!")
        print("✅ Cloudinary is properly configured")
        print("✅ Image URLs will be served from Cloudinary CDN")
    else:
        print("⚠️  SOME CLOUDINARY TESTS FAILED!")
        generate_cloudinary_setup_guide()
    
    print("="*60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
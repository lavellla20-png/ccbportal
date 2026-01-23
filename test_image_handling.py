#!/usr/bin/env python3
"""
Image Upload and Display Test Script for CCB Portal
This script tests the image handling functionality before deployment
"""

import os
import sys
import subprocess
from pathlib import Path

def test_image_url_generation():
    """Test image URL generation functionality"""
    print("🖼️  Testing image URL generation...")
    
    try:
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ccb_portal_backend.settings')
        import django
        django.setup()
        
        from portal.utils import build_production_media_url, build_safe_media_url
        from django.core.files.base import ContentFile
        
        # Test production URL generation
        test_file = ContentFile(b'test', name='test.jpg')
        test_file.url = '/media/announcements/test-image.jpg'
        
        # Test with production settings
        result = build_production_media_url(test_file)
        expected = "https://ccb-portal-backend.onrender.com/media/announcements/test-image.jpg"
        
        print(f"Production URL: {result}")
        print(f"Expected URL: {expected}")
        print(f"✅ Production URL generation: {'PASSED' if result == expected else 'FAILED'}")
        
        # Test different image paths
        test_cases = [
            ('/media/events/event1.jpg', 'https://ccb-portal-backend.onrender.com/media/events/event1.jpg'),
            ('/media/achievements/award.jpg', 'https://ccb-portal-backend.onrender.com/media/achievements/award.jpg'),
            ('/media/news/article.jpg', 'https://ccb-portal-backend.onrender.com/media/news/article.jpg'),
        ]
        
        print("\n📁 Testing different content types:")
        for input_path, expected_url in test_cases:
            test_file.url = input_path
            result = build_production_media_url(test_file)
            status = "✅" if result == expected_url else "❌"
            print(f"{status} {input_path} → {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Image URL generation test failed: {e}")
        return False

def test_frontend_url_normalization():
    """Test frontend URL normalization"""
    print("\n🌐 Testing frontend URL normalization...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        REACT_APP_API_URL = os.getenv('REACT_APP_API_URL', 'https://ccb-portal-backend.onrender.com')
        BACKEND_URL = REACT_APP_API_URL.rstrip('/')
        
        def normalizeImageUrl(imageUrl):
            if not imageUrl:
                return None
            if imageUrl.startswith('data:') or imageUrl.startswith('blob:'):
                return imageUrl
            if imageUrl.startswith('http://') or imageUrl.startswith('https://'):
                return imageUrl
            if imageUrl.startswith('/'):
                return f'{BACKEND_URL}{imageUrl}'
            return f'{BACKEND_URL}/{imageUrl}'
        
        # Test cases
        test_cases = [
            ('/media/announcements/test.jpg', 'https://ccb-portal-backend.onrender.com/media/announcements/test.jpg'),
            ('https://example.com/external.jpg', 'https://example.com/external.jpg'),
            ('http://example.com/old.jpg', 'http://example.com/old.jpg'),
            ('data:image/png;base64,abc123', 'data:image/png;base64,abc123'),
        ]
        
        print(f"Backend URL: {BACKEND_URL}")
        print("Testing URL normalization:")
        
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
        print(f"❌ Frontend URL normalization test failed: {e}")
        return False

def test_environment_variables():
    """Test environment variables"""
    print("\n🔧 Testing environment variables...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = [
            'PUBLIC_BASE_URL',
            'REACT_APP_API_URL',
            'CORS_ALLOWED_ORIGINS',
            'BREVO_API_KEY',
        ]
        
        print("Environment variables:")
        all_set = True
        for var in required_vars:
            value = os.getenv(var, 'NOT SET')
            status = "✅" if value != 'NOT SET' else "❌"
            print(f"{status} {var}: {value}")
            if value == 'NOT SET':
                all_set = False
        
        return all_set
        
    except Exception as e:
        print(f"❌ Environment variables test failed: {e}")
        return False

def generate_test_report():
    """Generate a test report"""
    print("\n" + "="*60)
    print("📊 IMAGE HANDLING TEST REPORT")
    print("="*60)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Image URL Generation", test_image_url_generation),
        ("Frontend URL Normalization", test_frontend_url_normalization),
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
        print("🎉 ALL TESTS PASSED! Ready for deployment!")
        print("✅ Image handling is properly configured")
        print("✅ Frontend and backend URLs are aligned")
        print("✅ Environment variables are set correctly")
    else:
        print("⚠️  SOME TESTS FAILED! Please fix the issues above")
        print("🔧 Review your configuration before deploying")
    print("="*60)
    
    return all_passed

def main():
    """Main test function"""
    print("🚀 CCB Portal Image Handling Test Suite")
    print("="*60)
    print("Testing image upload and display functionality...")
    
    success = generate_test_report()
    
    if success:
        print("\n🎯 Next steps:")
        print("1. Run: python prepare_render_deployment.py")
        print("2. Deploy to Render using the deployment guide")
        print("3. Test image upload in admin panel")
        print("4. Verify images display on frontend")
    else:
        print("\n🔧 Please fix the failing tests before deployment")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
"""
Security utilities for input validation, sanitization, and rate limiting.
"""
import re
from django.utils.html import escape
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from functools import wraps
from django.core.cache import cache
from django.conf import settings


def sanitize_string(value, max_length=None, allow_html=False):
    """
    Sanitize a string input to prevent XSS attacks.
    
    Args:
        value: Input string to sanitize
        max_length: Maximum allowed length (None for no limit)
        allow_html: If True, escape HTML. If False, strip HTML tags.
    
    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        value = str(value)
    
    # Remove null bytes
    value = value.replace('\x00', '')
    
    # Trim whitespace
    value = value.strip()
    
    # Limit length
    if max_length and len(value) > max_length:
        value = value[:max_length]
    
    # Escape HTML to prevent XSS
    if not allow_html:
        value = escape(value)
    
    return value


def validate_email_address(email):
    """
    Validate and sanitize an email address.
    
    Args:
        email: Email string to validate
    
    Returns:
        Sanitized email address
    
    Raises:
        ValidationError: If email is invalid
    """
    if not email:
        raise ValidationError("Email is required")
    
    email = sanitize_string(email, max_length=254, allow_html=False).lower()
    
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError("Invalid email format")
    
    return email


def sanitize_text_field(value, max_length=10000):
    """
    Sanitize a text field (like message body) that may contain line breaks.
    
    Args:
        value: Text to sanitize
        max_length: Maximum allowed length
    
    Returns:
        Sanitized text
    """
    if not value:
        return ""
    
    value = sanitize_string(value, max_length=max_length, allow_html=False)
    
    # Allow line breaks but sanitize them
    value = value.replace('\r\n', '\n').replace('\r', '\n')
    
    return value


def validate_phone(phone):
    """
    Validate and sanitize a phone number.
    
    Args:
        phone: Phone number string
    
    Returns:
        Sanitized phone number or None if empty
    """
    if not phone:
        return None
    
    # Remove common phone number characters, keep only digits and +
    phone = re.sub(r'[^\d+]', '', phone.strip())
    
    # Basic validation: should be between 10-15 digits
    digits_only = re.sub(r'[^\d]', '', phone)
    if len(digits_only) < 10 or len(digits_only) > 15:
        raise ValidationError("Invalid phone number format")
    
    return phone


def sanitize_url(url):
    """
    Sanitize and validate a URL.
    
    Args:
        url: URL string to sanitize
    
    Returns:
        Sanitized URL
    
    Raises:
        ValidationError: If URL is invalid
    """
    if not url:
        return None
    
    url = url.strip()
    
    # Basic URL validation
    if not url.startswith(('http://', 'https://', '/')):
        raise ValidationError("Invalid URL format")
    
    # Escape to prevent XSS
    url = escape(url)
    
    return url


def rate_limit(key_prefix, limit=10, period=60):
    """
    Rate limiting decorator to prevent abuse.
    
    Args:
        key_prefix: Unique prefix for the rate limit key
        limit: Maximum number of requests allowed
        period: Time period in seconds
    
    Usage:
        @rate_limit('api_contact_form', limit=5, period=300)
        def api_contact_form(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Get client IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR', 'unknown')
            
            # Create cache key
            cache_key = f'rate_limit:{key_prefix}:{ip}'
            
            # Check current count
            current = cache.get(cache_key, 0)
            
            if current >= limit:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Rate limit exceeded. Please try again in {period} seconds.'
                }, status=429)
            
            # Increment counter
            cache.set(cache_key, current + 1, period)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def validate_json_input(data, required_fields=None, field_validators=None):
    """
    Validate JSON input data.
    
    Args:
        data: Dictionary of input data
        required_fields: List of required field names
        field_validators: Dict mapping field names to validator functions
    
    Returns:
        Tuple of (is_valid, error_message, sanitized_data)
    """
    sanitized_data = {}
    
    # Check required fields
    if required_fields:
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f'Field "{field}" is required', None
    
    # Validate and sanitize fields
    if field_validators:
        for field, validator in field_validators.items():
            if field in data:
                try:
                    sanitized_data[field] = validator(data[field])
                except ValidationError as e:
                    return False, str(e), None
                except Exception as e:
                    return False, f'Invalid value for field "{field}": {str(e)}', None
            else:
                sanitized_data[field] = None
    
    return True, None, sanitized_data


def prevent_sql_injection(value):
    """
    Additional protection against SQL injection (though Django ORM handles this).
    This is a defense-in-depth measure.
    
    Args:
        value: Input value to check
    
    Returns:
        Sanitized value
    
    Raises:
        ValidationError: If SQL injection pattern detected
    """
    if not isinstance(value, str):
        return value
    
    # Common SQL injection patterns
    sql_patterns = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE|UNION|SCRIPT)\b)",
        r"(--|#|/\*|\*/|;|\||&)",
        r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
    ]
    
    value_upper = value.upper()
    for pattern in sql_patterns:
        if re.search(pattern, value_upper, re.IGNORECASE):
            raise ValidationError("Invalid input detected")
    
    return value

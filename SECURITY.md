# Security Hardening Guide

This document outlines the security measures implemented in the CCB Portal application.

## Overview

The application has been hardened against common web vulnerabilities including:
- SQL Injection
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Clickjacking
- Brute Force Attacks
- Information Disclosure

## Backend Security (Django)

### 1. Environment Variables

**CRITICAL**: Never commit sensitive data to version control. All secrets must be stored in environment variables.

Create a `.env` file in the project root with the following variables:

```bash
# Django Secret Key (generate a new one!)
DJANGO_SECRET_KEY=your-secret-key-here

# Debug Mode (set to False in production)
DEBUG=False

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database Configuration
DB_NAME=ccb_portal
DB_USER=root
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=3306

# CORS Configuration
CORS_ALLOWED_ORIGINS=https://yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com

# Email Configuration
BREVO_API_KEY=your-api-key
EMAIL_HOST_USER=your-email-user
EMAIL_HOST_PASSWORD=your-email-password
```

### 2. Security Settings

The following security settings are configured in `settings.py`:

- **X-Frame-Options**: Set to `DENY` to prevent clickjacking
- **XSS Protection**: Browser XSS filter enabled
- **Content-Type Sniffing**: Disabled to prevent MIME type confusion
- **HTTPS**: SSL redirect enabled in production
- **HSTS**: HTTP Strict Transport Security enabled (1 year)
- **Secure Cookies**: Session and CSRF cookies are secure in production
- **HTTPOnly Cookies**: Session cookies are HTTPOnly

### 3. Input Validation and Sanitization

All user inputs are validated and sanitized using utilities in `portal/security.py`:

- **String Sanitization**: HTML escaping to prevent XSS
- **Email Validation**: Proper email format validation
- **Phone Validation**: Format and length validation
- **SQL Injection Prevention**: Pattern detection and sanitization
- **Length Limits**: Maximum length restrictions on all text fields

### 4. Rate Limiting

Rate limiting is implemented to prevent brute force attacks:

- **Contact Form**: 5 requests per 5 minutes per IP
- **Admin Login**: 5 attempts per 5 minutes per IP

### 5. CSRF Protection

- CSRF protection is enabled for all authenticated endpoints
- Public API endpoints (like contact form) use `@csrf_exempt` but include rate limiting
- CSRF tokens are automatically handled by Django middleware

### 6. Database Security

- Django ORM is used exclusively (no raw SQL queries)
- Parameterized queries prevent SQL injection
- Database credentials stored in environment variables
- Strict SQL mode enabled

## Frontend Security (React)

### 1. Input Sanitization

All user inputs are sanitized using utilities in `src/utils/security.js`:

- **XSS Prevention**: HTML entity escaping
- **Input Validation**: Email, phone, URL validation
- **Length Limits**: Maximum length restrictions

### 2. CSRF Token Handling

CSRF tokens are automatically included in API requests:

- Tokens are read from cookies
- Automatically added to POST/PUT/DELETE requests
- Handled transparently by the API service

### 3. Content Security

- User-generated content is escaped before display
- URLs are validated before use
- No `dangerouslySetInnerHTML` without sanitization

## Security Best Practices

### For Development

1. **Never commit `.env` file** - Add it to `.gitignore`
2. **Use different secrets** for development and production
3. **Keep DEBUG=False** in production
4. **Use strong passwords** for database and admin accounts

### For Production

1. **Use HTTPS** - SSL/TLS certificates required
2. **Set DEBUG=False** - Prevents information disclosure
3. **Restrict ALLOWED_HOSTS** - Only your domain(s)
4. **Use environment variables** - Never hardcode secrets
5. **Regular updates** - Keep Django and dependencies updated
6. **Monitor logs** - Watch for suspicious activity
7. **Backup database** - Regular backups with encryption
8. **Use strong SECRET_KEY** - Generate a new one for production

### Generating a Secure Secret Key

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Security Checklist

Before deploying to production:

- [ ] All secrets moved to environment variables
- [ ] DEBUG set to False
- [ ] ALLOWED_HOSTS configured correctly
- [ ] HTTPS enabled and working
- [ ] Database password is strong
- [ ] Admin accounts use strong passwords
- [ ] CORS origins restricted
- [ ] CSRF trusted origins configured
- [ ] Rate limiting tested
- [ ] Input validation tested
- [ ] Error messages don't leak sensitive info
- [ ] Logs don't contain sensitive data
- [ ] `.env` file is in `.gitignore`

## Reporting Security Issues

If you discover a security vulnerability, please report it responsibly:
1. Do not create a public issue
2. Contact the development team directly
3. Provide detailed information about the vulnerability
4. Allow time for the issue to be fixed before disclosure

## Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

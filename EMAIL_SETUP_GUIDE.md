# Email Configuration Guide - BREVO Setup

## Error: "5.7.0 Please authenticate first"

This error occurs when BREVO email service requires authentication but the credentials are not properly configured.

## Solution

You need to set up BREVO API key in your environment variables. Here's how:

### Option 1: Using BREVO API (Recommended)

1. **Get your BREVO API Key:**
   - Go to https://app.brevo.com/
   - Log in to your account
   - Navigate to **Settings** → **SMTP & API**
   - Copy your **API Key** (v3 API key)

2. **Set Environment Variable:**
   
   **Windows (PowerShell):**
   ```powershell
   $env:BREVO_API_KEY="your-api-key-here"
   ```
   
   **Windows (CMD):**
   ```cmd
   set BREVO_API_KEY=your-api-key-here
   ```
   
   **Linux/Mac:**
   ```bash
   export BREVO_API_KEY="your-api-key-here"
   ```

3. **Restart Django Server:**
   - Stop the Django server (Ctrl+C)
   - Start it again: `python manage.py runserver`

### Option 2: Using SMTP (Fallback)

If you prefer to use SMTP instead of the API:

1. **Get SMTP Credentials from BREVO:**
   - Go to https://app.brevo.com/
   - Navigate to **Settings** → **SMTP & API**
   - Note your SMTP server, port, and login credentials

2. **Set Environment Variables:**
   
   **Windows (PowerShell):**
   ```powershell
   $env:EMAIL_HOST="smtp-relay.brevo.com"
   $env:EMAIL_PORT="587"
   $env:EMAIL_USE_TLS="True"
   $env:EMAIL_HOST_USER="your-smtp-username@brevo.com"
   $env:EMAIL_HOST_PASSWORD="your-smtp-password"
   $env:DEFAULT_FROM_EMAIL="citycollegeofbayawan@gmail.com"
   ```
   
   **Windows (CMD):**
   ```cmd
   set EMAIL_HOST=smtp-relay.brevo.com
   set EMAIL_PORT=587
   set EMAIL_USE_TLS=True
   set EMAIL_HOST_USER=your-smtp-username@brevo.com
   set EMAIL_HOST_PASSWORD=your-smtp-password
   set DEFAULT_FROM_EMAIL=citycollegeofbayawan@gmail.com
   ```
   
   **Linux/Mac:**
   ```bash
   export EMAIL_HOST="smtp-relay.brevo.com"
   export EMAIL_PORT="587"
   export EMAIL_USE_TLS="True"
   export EMAIL_HOST_USER="your-smtp-username@brevo.com"
   export EMAIL_HOST_PASSWORD="your-smtp-password"
   export DEFAULT_FROM_EMAIL="citycollegeofbayawan@gmail.com"
   ```

3. **Make sure BREVO_API_KEY is NOT set** (or set to empty) to use SMTP fallback

### Option 3: Using .env File (Recommended for Production)

Create a `.env` file in your project root:

```env
BREVO_API_KEY=your-api-key-here
DEFAULT_FROM_EMAIL=citycollegeofbayawan@gmail.com
CONTACT_INBOX=citycollegeofbayawan@gmail.com
PUBLIC_BASE_URL=http://localhost:8000
```

Then install `python-dotenv`:
```bash
pip install python-dotenv
```

And update `settings.py` to load it:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Verification

After setting up, test the email configuration:

1. Try submitting the contact form again
2. Check Django logs for any errors
3. Check your BREVO dashboard for sent emails

## Troubleshooting

### Error: "Please authenticate first"
- **Cause**: BREVO API key not set or invalid
- **Solution**: Set `BREVO_API_KEY` environment variable with a valid API key

### Error: "SMTP authentication failed"
- **Cause**: SMTP credentials incorrect or missing
- **Solution**: Set `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` environment variables

### Error: "Template not found"
- **Cause**: BREVO template ID is incorrect
- **Solution**: Check `BREVO_TEMPLATE_VERIFY_ID` environment variable or use the default template

### Emails not sending
- Check BREVO account status
- Verify sender email is verified in BREVO
- Check BREVO account limits/quota
- Review Django logs for detailed error messages

## Current Configuration

The application will:
1. **First try**: BREVO API with template (if `BREVO_API_KEY` is set)
2. **Fallback**: SMTP with HTML email (if BREVO API fails or not configured)
3. **Last resort**: Console backend (for development only)

## Security Notes

- **Never commit API keys or passwords to Git**
- Use environment variables or `.env` file (add to `.gitignore`)
- Rotate API keys regularly
- Use different keys for development and production

## Support

If issues persist:
1. Check BREVO dashboard for account status
2. Verify email address is verified in BREVO
3. Check BREVO API/SMTP quotas
4. Review Django logs: `python manage.py runserver --verbosity 2`


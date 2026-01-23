# CCB Portal Production Deployment Guide

This guide will help you deploy the CCB Portal application to Render with proper image handling between frontend and backend.

## Environment Variables

### Backend (ccb-portal-backend.onrender.com)

Set these environment variables in your Render backend service:

```bash
# Django Settings
DJANGO_SETTINGS_MODULE=ccb_portal_backend.production_settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False

# Database (Render will provide this)
DATABASE_URL=postgresql://username:password@host:port/database

# URLs
PUBLIC_BASE_URL=https://ccb-portal-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://ccb-portal-frontend.onrender.com

# Email (Brevo)
BREVO_API_KEY=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
DEFAULT_FROM_EMAIL=citycollegeofbayawan@gmail.com
SERVER_EMAIL=citycollegeofbayawan@gmail.com
CONTACT_INBOX=citycollegeofbayawan@gmail.com

# Optional: Redis for caching (if you want to add Redis to your Render setup)
# REDIS_URL=redis://username:password@host:port
```

### Frontend (ccb-portal-frontend.onrender.com)

Set these environment variables in your Render frontend service:

```bash
# API Configuration
REACT_APP_API_URL=https://ccb-portal-backend.onrender.com

# Build settings (if needed)
CI=false
GENERATE_SOURCEMAP=false
```

## Deployment Steps

### 1. Backend Deployment

1. **Create Web Service on Render:**
   - Connect your GitHub repository
   - Select the backend branch
   - Set environment variables as listed above
   - Use these build and start commands:
     ```bash
     # Build command
     pip install -r requirements.txt
     
     # Start command
     python manage.py migrate && python manage.py collectstatic --noinput && gunicorn ccb_portal_backend.wsgi:application
     ```

2. **Verify Backend Deployment:**
   - Check that the backend is accessible at `https://ccb-portal-backend.onrender.com`
   - Test the API endpoint: `https://ccb-portal-backend.onrender.com/api/test/`

### 2. Frontend Deployment

1. **Create Static Site on Render:**
   - Connect your GitHub repository
   - Select the frontend branch (or same branch if using monorepo)
   - Set environment variables as listed above
   - Use these build and publish settings:
     ```bash
     # Build command
     npm install && npm run build
     
     # Publish directory
     build
     ```

2. **Verify Frontend Deployment:**
   - Check that the frontend is accessible at `https://ccb-portal-frontend.onrender.com`
   - Verify that API calls are working correctly

### 3. Image Upload Testing

1. **Test Image Upload:**
   - Access the admin panel at `https://ccb-portal-backend.onrender.com/admin/`
   - Create a test announcement, event, achievement, or news item with an image
   - Save the item

2. **Test Image Display:**
   - Visit the frontend at `https://ccb-portal-frontend.onrender.com`
   - Check that the uploaded image displays correctly
   - Verify that image URLs are pointing to the backend domain

## Image URL Configuration

The application has been configured to handle image URLs correctly in production:

### Backend Configuration

- **Media URL Construction**: The backend now uses `build_production_media_url()` function to create absolute URLs for images
- **CORS**: Configured to allow requests from your frontend domain
- **Static/Media Serving**: Django serves media files with proper URLs

### Frontend Configuration

- **Image URL Normalization**: The `normalizeImageUrl()` function in `src/utils/imageUtils.js` handles both relative and absolute URLs
- **API Base URL**: Uses `REACT_APP_API_URL` environment variable to construct proper backend URLs

## Troubleshooting

### Images Not Displaying

1. **Check Environment Variables:**
   - Verify `REACT_APP_API_URL` is set correctly on frontend
   - Verify `PUBLIC_BASE_URL` is set correctly on backend

2. **Check CORS:**
   - Ensure `CORS_ALLOWED_ORIGINS` includes your frontend URL
   - Check browser console for CORS errors

3. **Check Image URLs:**
   - Inspect image URLs in browser developer tools
   - Verify they point to `https://ccb-portal-backend.onrender.com/media/...`

4. **Check File Uploads:**
   - Verify images are being uploaded to the backend
   - Check Render logs for upload errors

### Common Issues

1. **Mixed Content Errors:**
   - Ensure both frontend and backend use HTTPS
   - Check that all image URLs use `https://`

2. **CORS Errors:**
   - Verify CORS_ALLOWED_ORIGINS includes exact frontend URL
   - Check for trailing slashes in URLs

3. **Image Upload Failures:**
   - Check file size limits (currently 10MB)
   - Verify file types are allowed (images only)

## Testing Script

Use the provided deployment script to verify your configuration:

```bash
python deploy_production.py
```

This script will:
- Check environment variables
- Verify Django settings
- Test media configuration
- Run migrations
- Collect static files

## Security Considerations

1. **File Upload Security:**
   - Only image files are allowed (JPG, PNG, GIF, WebP)
   - File size is limited to 10MB
   - Files are validated for proper MIME types

2. **CORS Security:**
   - Only your specific frontend domain is allowed
   - Credentials are properly handled

3. **Production Settings:**
   - DEBUG is disabled
   - Security headers are enabled
   - HTTPS is enforced

## Support

If you encounter issues:

1. Check Render logs for both frontend and backend
2. Verify all environment variables are set correctly
3. Test the deployment script to identify configuration issues
4. Check browser developer tools for network errors
5. Ensure both services are properly connected and communicating
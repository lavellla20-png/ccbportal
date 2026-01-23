# 🚀 Complete Render Deployment Guide for CCB Portal

This guide will walk you through deploying your CCB Portal application to Render with proper image handling between frontend and backend.

## 📋 Prerequisites

Before starting, ensure you have:
- GitHub account with your repository
- Render account (free tier works)
- Your code pushed to GitHub (✅ Already done)

## 🎯 Deployment Overview

**Backend**: Django API serving at `https://ccb-portal-backend.onrender.com`
**Frontend**: React app at `https://ccb-portal-frontend.onrender.com`
**Image Flow**: Backend uploads → Frontend displays via cross-domain URLs

---

## 🔧 Step 1: Backend Deployment (ccb-portal-backend)

### 1.1 Create Web Service on Render

1. **Login to Render** → [render.com](https://render.com)
2. **Click "New"** → **Web Service**
3. **Connect GitHub** → Select your `ccbwebmain` repository
4. **Configure Service:**

```yaml
Name: ccb-portal-backend
Branch: main
Root Directory: . (leave empty)
Build Command: pip install -r requirements.txt
Start Command: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn ccb_portal_backend.wsgi:application
Instance Type: Free (or paid if you prefer)
```

### 1.2 Set Environment Variables

**Add these environment variables in Render dashboard:**

```bash
# Django Configuration
DJANGO_SETTINGS_MODULE=ccb_portal_backend.production_settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False

# Database (Render provides this automatically)
DATABASE_URL=postgresql://username:password@host:port/database

# URLs & CORS
PUBLIC_BASE_URL=https://ccb-portal-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://ccb-portal-frontend.onrender.com

# Email Configuration
BREVO_API_KEY=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
DEFAULT_FROM_EMAIL=citycollegeofbayawan@gmail.com
SERVER_EMAIL=citycollegeofbayawan@gmail.com
CONTACT_INBOX=citycollegeofbayawan@gmail.com

# Optional: Redis (if you add Redis later)
# REDIS_URL=redis://username:password@host:port
```

### 1.3 Deploy Backend

1. **Click "Create Web Service"**
2. **Wait for deployment** (2-5 minutes)
3. **Test the API**: Visit `https://ccb-portal-backend.onrender.com/api/test/`
4. **Create superuser**: `python manage.py createsuperuser` (via Render shell)

---

## 🎨 Step 2: Frontend Deployment (ccb-portal-frontend)

### 2.1 Create Static Site on Render

1. **Go to Render Dashboard**
2. **Click "New"** → **Static Site**
3. **Connect GitHub** → Select same repository
4. **Configure Frontend:**

```yaml
Name: ccb-portal-frontend
Branch: main
Build Command: npm install && npm run build
Publish Directory: build
```

### 2.2 Set Environment Variables

**Add these environment variables:**

```bash
# API Configuration
REACT_APP_API_URL=https://ccb-portal-backend.onrender.com

# Build Settings
CI=false
GENERATE_SOURCEMAP=false
```

### 2.3 Deploy Frontend

1. **Click "Create Static Site"**
2. **Wait for build** (3-7 minutes)
3. **Access your site**: `https://ccb-portal-frontend.onrender.com`

---

## 🧪 Step 3: Image Upload & Display Testing

### 3.1 Test Image Upload

1. **Access Admin Panel**: `https://ccb-portal-backend.onrender.com/admin/`
2. **Login with superuser credentials**
3. **Create Test Content:**
   - Go to "Announcements" → Add new
   - Fill title, date, body
   - Upload an image (JPG/PNG, max 10MB)
   - Save

### 3.2 Test Image Display

1. **Visit Frontend**: `https://ccb-portal-frontend.onrender.com`
2. **Check Homepage**: Look for your announcement with image
3. **Check News/Events Page**: Test different content types
4. **Verify Image URLs**: Right-click image → "Copy image address"
   - Should show: `https://ccb-portal-backend.onrender.com/media/announcements/filename.jpg`

---

## 🔍 Step 4: Troubleshooting Common Issues

### ❌ Images Not Displaying

**Check 1: Environment Variables**
```bash
# Backend should have:
PUBLIC_BASE_URL=https://ccb-portal-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://ccb-portal-frontend.onrender.com

# Frontend should have:
REACT_APP_API_URL=https://ccb-portal-backend.onrender.com
```

**Check 2: CORS Errors**
- Open browser console (F12)
- Look for "CORS policy" errors
- Ensure backend CORS allows frontend URL

**Check 3: Image URLs**
- Inspect image element in browser
- Verify URL starts with `https://ccb-portal-backend.onrender.com/media/`
- Check for mixed content (HTTP vs HTTPS)

### ❌ Image Upload Fails

**Check File Size**: Max 10MB per image
**Check File Type**: Only JPG, PNG, GIF, WebP allowed
**Check Backend Logs**: Render dashboard → Logs tab

### ❌ Mixed Content Errors

**Symptoms**: Browser blocks images due to HTTP/HTTPS mismatch
**Solution**: Ensure both frontend and backend use HTTPS
**Check**: All image URLs should start with `https://`

---

## 🛠️ Step 5: Advanced Configuration

### 5.1 Custom Domain Setup (Optional)

**Backend Custom Domain:**
```bash
# Add to backend environment variables
ALLOWED_HOSTS=your-backend-domain.com,ccb-portal-backend.onrender.com
PUBLIC_BASE_URL=https://your-backend-domain.com
```

**Frontend Custom Domain:**
```bash
# Update CORS in backend
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com

# Update frontend
REACT_APP_API_URL=https://your-backend-domain.com
```

### 5.2 Performance Optimization

**Enable CDN for Images:**
- Consider Cloudinary integration (already partially configured)
- Or use Render's built-in CDN

**Database Optimization:**
```bash
# Add to backend environment
DATABASE_CONN_MAX_AGE=600
DATABASE_CONN_HEALTH_CHECKS=True
```

---

## 📊 Step 6: Monitoring & Maintenance

### 6.1 Check Application Health

**Backend Health Check:**
```bash
curl https://ccb-portal-backend.onrender.com/api/test/
```

**Frontend Health Check:**
```bash
curl https://ccb-portal-frontend.onrender.com
```

### 6.2 Monitor Logs

**Render Dashboard Logs:**
- Check both services regularly
- Look for upload errors, CORS issues
- Monitor response times

### 6.3 Regular Maintenance

**Monthly Tasks:**
- Check disk usage (media files accumulate)
- Update dependencies
- Review security logs
- Test backup/restore procedures

---

## 🚨 Emergency Procedures

### Backend Down
1. Check Render status page
2. Review recent deployments
3. Check environment variables
4. Rollback if necessary

### Frontend Down
1. Check build logs in Render
2. Verify API connectivity
3. Check for JavaScript errors
4. Test locally first

### Images Not Loading
1. Check backend media directory
2. Verify CORS settings
3. Test image URLs directly
4. Check file permissions

---

## 📞 Support Resources

**Render Documentation:** [docs.render.com](https://docs.render.com)
**Django Documentation:** [docs.djangoproject.com](https://docs.djangoproject.com)
**React Documentation:** [reactjs.org/docs](https://reactjs.org/docs)

**Need Help?**
- Check your deployment script: `python deploy_production.py`
- Review logs in Render dashboard
- Test configuration locally first

---

## ✅ Deployment Checklist

**Before Going Live:**
- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Image upload working from admin
- [ ] Images display correctly on frontend
- [ ] CORS working (no browser errors)
- [ ] HTTPS enforced on both services
- [ ] Environment variables set correctly
- [ ] Admin credentials created
- [ ] Test content added with images
- [ ] Cross-browser testing completed
- [ ] Mobile responsiveness verified

**Congratulations!** 🎉 Your CCB Portal is now ready for production!
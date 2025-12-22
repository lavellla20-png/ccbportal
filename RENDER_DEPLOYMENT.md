# Render.com Deployment Guide

This guide will walk you through deploying the City College of Bayawan web portal to Render.com.

## 📋 Prerequisites

1. A Render.com account (sign up at https://render.com)
2. Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)
3. Environment variables ready (see below)

## 🗄️ Architecture Overview

The deployment consists of:
- **PostgreSQL Database**: Managed PostgreSQL service
- **Django Backend**: Web service running Django + Gunicorn
- **React Frontend**: Built and served as static files by Django

## 🚀 Step-by-Step Deployment

### Option 1: Using render.yaml (Recommended)

1. **Push your code to Git**
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. **Connect Repository to Render**
   - Go to https://dashboard.render.com
   - Click "New +" → "Blueprint"
   - Connect your Git repository
   - Render will detect `render.yaml` automatically

3. **Configure Environment Variables**
   After the services are created, go to each service and set:
   
   **For Backend Service (`ccb-portal-backend`):**
   - `ALLOWED_HOSTS`: Your Render backend URL (e.g., `ccb-portal-backend.onrender.com`)
   - `CORS_ALLOWED_ORIGINS`: Your frontend URL (same as backend URL since Django serves React)
   - `BREVO_API_KEY`: (Optional) Your Brevo email API key if using email features
   - `DJANGO_SECRET_KEY`: Auto-generated, but you can set a custom one

4. **Deploy**
   - Render will automatically deploy when you connect the repository
   - Monitor the build logs in the Render dashboard

### Option 2: Manual Setup

#### Step 1: Create PostgreSQL Database

1. Go to Render Dashboard → "New +" → "PostgreSQL"
2. Configure:
   - **Name**: `ccb-portal-db`
   - **Database**: `ccb_portal`
   - **User**: `ccb_user`
   - **Plan**: Free (or choose a paid plan)
3. Click "Create Database"
4. **Save the Internal Database URL** (you'll need it later)

#### Step 2: Create Django Web Service

1. Go to Render Dashboard → "New +" → "Web Service"
2. Connect your Git repository
3. Configure the service:

   **Basic Settings:**
   - **Name**: `ccb-portal-backend`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (root of repo)

   **Build & Deploy:**
   - **Build Command**: 
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt && npm install && npm run build && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```bash
     python manage.py migrate && gunicorn ccb_portal_backend.wsgi:application
     ```

   **Environment Variables:**
   Add these environment variables:
   ```
   PYTHON_VERSION=3.11.0
   DJANGO_SECRET_KEY=<generate-a-secret-key>
   DJANGO_DEBUG=False
   ALLOWED_HOSTS=ccb-portal-backend.onrender.com
   CORS_ALLOWED_ORIGINS=https://ccb-portal-backend.onrender.com
   DATABASE_URL=<from-postgres-service-internal-database-url>
   SECURE_SSL_REDIRECT=True
   DEFAULT_FROM_EMAIL=citycollegeofbayawan@gmail.com
   BREVO_API_KEY=<your-brevo-api-key-if-using-email>
   ```

4. Click "Create Web Service"

#### Step 3: Update Environment Variables

After the service is created:

1. Go to your web service → "Environment"
2. Update `ALLOWED_HOSTS` with your actual Render URL (found in the service overview)
3. Update `CORS_ALLOWED_ORIGINS` with the same URL
4. Add the `DATABASE_URL` from your PostgreSQL service (use the Internal Database URL)

## 🔧 Post-Deployment Setup

### 1. Run Database Migrations

Migrations should run automatically via the start command, but you can also run them manually:

1. Go to your web service → "Shell"
2. Run:
   ```bash
   python manage.py migrate
   ```

### 2. Create Superuser

1. Go to your web service → "Shell"
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Follow the prompts to create an admin user

### 4. Access Your Application

- **Frontend**: `https://your-service-name.onrender.com`
- **Admin Panel**: `https://your-service-name.onrender.com/admin`
- **API**: `https://your-service-name.onrender.com/api`

## 🔐 Environment Variables Reference

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | Auto-generated or custom |
| `DJANGO_DEBUG` | Debug mode | `False` for production |
| `ALLOWED_HOSTS` | Allowed hostnames | `your-app.onrender.com` |
| `DATABASE_URL` | PostgreSQL connection string | Auto-provided by Render |
| `CORS_ALLOWED_ORIGINS` | Allowed CORS origins | `https://your-app.onrender.com` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BREVO_API_KEY` | Brevo email API key | Empty (uses console backend) |
| `DEFAULT_FROM_EMAIL` | Default sender email | `citycollegeofbayawan@gmail.com` |
| `SECURE_SSL_REDIRECT` | Force HTTPS | `True` |
| `CORS_ALLOWED_ORIGINS` | CORS origins | Set to your domain |

## 📝 Important Notes

### Database Migration

- The app uses PostgreSQL on Render (not MySQL)
- Database migrations run automatically on startup
- Make sure all migrations are committed to your repository

### Static Files

- React build files are collected into Django's `staticfiles` directory
- WhiteNoise serves static files in production
- Media files (uploads) are stored in the `media` directory (consider using S3 for production)

### Media Files Storage

⚠️ **Important**: Render's filesystem is ephemeral. Uploaded media files will be lost on redeploy.

**Solutions:**
1. **Use AWS S3** (Recommended for production)
   - Install `django-storages` and `boto3`
   - Configure Django to use S3 for media files
   
2. **Use Render Disk** (Paid feature)
   - Add a persistent disk to your service
   - Mount it for media storage

3. **Use External Storage Service**
   - Cloudinary, Cloudflare R2, or similar

### CORS Configuration

Since Django serves the React frontend, CORS should include your Render domain:
```
CORS_ALLOWED_ORIGINS=https://your-app.onrender.com
```

### SSL/HTTPS

Render provides SSL certificates automatically. Set `SECURE_SSL_REDIRECT=True` to enforce HTTPS.

## 🐛 Troubleshooting

### Build Fails

1. **Check build logs** in Render dashboard
2. **Common issues:**
   - Missing dependencies in `requirements.txt`
   - Node.js version mismatch
   - Build script errors

### Database Connection Errors

1. Verify `DATABASE_URL` is set correctly
2. Use the **Internal Database URL** from PostgreSQL service
3. Check that PostgreSQL service is running

### Static Files Not Loading

1. Verify `collectstatic` ran successfully
2. Check `STATIC_ROOT` in settings.py
3. Ensure WhiteNoise middleware is enabled

### 500 Errors

1. Check application logs in Render dashboard
2. Verify all environment variables are set
3. Check database migrations completed successfully
4. Ensure `ALLOWED_HOSTS` includes your domain

### CORS Errors

1. Verify `CORS_ALLOWED_ORIGINS` includes your frontend URL
2. Check that CORS middleware is enabled
3. Ensure credentials are handled correctly

## 📊 Monitoring

- **Logs**: View real-time logs in Render dashboard
- **Metrics**: Monitor CPU, memory, and request metrics
- **Health Checks**: Configure health check endpoint (`/admin/`)

## 🔄 Updating Your Application

1. **Push changes to Git**
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```

2. **Render automatically deploys** (if auto-deploy is enabled)
3. **Or manually deploy** from Render dashboard

## 💰 Cost Considerations

### Free Tier Limits

- **Web Services**: Spins down after 15 minutes of inactivity
- **PostgreSQL**: 90-day retention, 1GB storage
- **Build Time**: Limited build minutes per month

### Paid Plans

Consider upgrading for:
- Always-on services (no spin-down)
- More database storage
- Better performance
- Custom domains

## 🔗 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Django on Render](https://render.com/docs/deploy-django)
- [PostgreSQL on Render](https://render.com/docs/databases)
- [Environment Variables](https://render.com/docs/environment-variables)

## 📞 Support

If you encounter issues:
1. Check Render dashboard logs
2. Review Django logs in the service shell
3. Verify environment variables
4. Check Render status page

---

**Note**: This deployment configuration assumes Django serves both the API and the React frontend. The React app is built and served as static files through Django's static file handling.


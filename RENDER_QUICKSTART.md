# Render.com Quick Start Guide

## 🚀 Fast Deployment (5 Minutes)

### Step 1: Prepare Your Code

1. **Commit all changes:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

### Step 2: Deploy on Render

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +" → "Blueprint"**
3. **Connect your Git repository**
4. **Render will detect `render.yaml` automatically**
5. **Click "Apply"**

### Step 3: Configure Environment Variables

After services are created, go to **ccb-portal-backend** service → **Environment**:

1. **Set `ALLOWED_HOSTS`**: 
   - Value: `your-service-name.onrender.com` (check your service URL)
   
2. **Set `CORS_ALLOWED_ORIGINS`**: 
   - Value: `https://your-service-name.onrender.com` (same as above)

3. **Optional - Set `BREVO_API_KEY`**:
   - Only if you're using email features

### Step 4: Create Admin User

1. Go to **ccb-portal-backend** → **Shell**
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Follow prompts to create admin account

### Step 5: Access Your App

- **Frontend**: `https://your-service-name.onrender.com`
- **Admin**: `https://your-service-name.onrender.com/admin`

## ✅ That's It!

Your app should now be live. Check the logs if you encounter any issues.

## 🔧 Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Ensure `requirements.txt` has all dependencies
- Verify Node.js version compatibility

### Database Errors
- Verify `DATABASE_URL` is set (auto-set by Render)
- Check PostgreSQL service is running
- Run migrations manually: `python manage.py migrate`

### 500 Errors
- Check application logs
- Verify `ALLOWED_HOSTS` matches your domain
- Ensure all environment variables are set

## 📚 Full Documentation

See `RENDER_DEPLOYMENT.md` for detailed information.


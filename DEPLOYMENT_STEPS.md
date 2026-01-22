# 🚀 Deployment Steps for Image Loading Fix

## Prerequisites
- Git repository with changes committed
- Access to Render dashboard

## Step 1: Commit Changes
```bash
git add ccb_portal_backend/settings.py portal/utils.py IMAGE_LOADING_FIX.md
git commit -m "Fix: Image loading from Cloudinary to static frontend site

- Updated build_safe_media_url() to properly handle Cloudinary URLs
- Added Cloudinary HTTPS configuration
- Added CORS origin for static frontend site"
git push
```

## Step 2: Deploy to Render

### Option A: Automatic Deployment (Recommended)
If you have Render connected to your Git repo:
1. Go to: https://dashboard.render.com/
2. Click on **ccb-portal-backend** service
3. Go to **Deployments** tab
4. The new deployment should start automatically
5. Wait for "Deploy successful" message (2-5 minutes)
6. Check status indicates "Live"

### Option B: Manual Deployment (If auto-deploy not enabled)
1. Go to: https://dashboard.render.com/
2. Click on **ccb-portal-backend** service
3. Click **"Manual Deploy"** button
4. Select **main** branch
5. Click **Deploy**
6. Wait for deployment to complete

## Step 3: Verify Deployment

### Test API Endpoint
1. Open: https://ccb-portal-backend.onrender.com/api/news/
2. Check response JSON
3. Look for `"image"` field - should contain full Cloudinary URL like:
   ```
   "image": "https://res.cloudinary.com/dvodewe6g/image/upload/..."
   ```
4. If you see this, the fix is working! ✅

### Test Frontend Display
1. Go to: https://ccb-portal-static.onrender.com/
2. Navigate to **News** or **Events** section
3. Images should display properly
4. Open browser DevTools (F12) → Network tab
5. Check that image requests are successful (200 OK, not 404 or CORS errors)

### Check Backend Logs
1. Go to Render dashboard: https://dashboard.render.com/
2. Click **ccb-portal-backend** service
3. Click **Logs** tab
4. Look for any errors related to:
   - Cloudinary configuration
   - Image URL generation
   - Should see no errors if fix is working

## Step 4: Troubleshooting (If Images Still Don't Load)

### Issue: Still seeing broken images
**Check 1: Clear browser cache**
- Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
- Clear DevTools cache

**Check 2: Verify Cloudinary credentials**
- Go to settings.py
- Ensure CLOUDINARY_CLOUD_NAME, API_KEY, and API_SECRET are set
- Check Cloudinary dashboard at https://cloudinary.com/console/

**Check 3: Check CORS errors in browser console**
- Open browser DevTools (F12)
- Check Console and Network tabs
- If CORS error, verify https://ccb-portal-static.onrender.com is in CORS_ALLOWED_ORIGINS

**Check 4: Re-upload images**
1. Go to Django admin: https://ccb-portal-backend.onrender.com/admin/
2. Click on News item
3. Re-upload the image (even if it exists)
4. Save and test

## Step 5: After Successful Deployment

### Verify Everything Works
- [ ] Images display on News page
- [ ] Images display on Events page
- [ ] Images display on Achievements page
- [ ] Admin can still upload images
- [ ] API returns Cloudinary URLs
- [ ] No CORS errors in browser console
- [ ] Backend logs show no errors

### Commit Success (Optional)
```bash
git log -1  # Verify your commit is deployed
```

## Rollback (If needed)
If something goes wrong:
1. Go to Render dashboard
2. Click **ccb-portal-backend**
3. Click **Deployments** tab
4. Find the previous successful deployment
5. Click the three-dot menu
6. Select **Rollback**

---

**Questions?** Check the IMAGE_LOADING_FIX.md file for detailed explanation of what was changed and why.

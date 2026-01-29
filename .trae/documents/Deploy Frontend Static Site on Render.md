To deploy your **Static Site (Frontend)** on Render's Free Tier, follow these exact steps. I have tailored this to your React project structure.

### 1. Configuration Settings (Fill these in the form)

*   **Name:** `ccbeacademyportal-frontend` (or any unique name you prefer, e.g., `ccb-frontend-new`)
*   **Repository:** `lavellla20-png/ccbportal`
*   **Branch:** `main`
*   **Root Directory:** `.` (Leave empty or enter `.`)
*   **Build Command:** `npm install && npm run build`
*   **Publish Directory:** `build`

### 2. Environment Variables (Critical Step)
You must add the environment variable to tell the frontend where your backend is located.

1.  Scroll down to **Environment Variables**.
2.  Add a new variable:
    *   **Key:** `REACT_APP_API_URL`
    *   **Value:** `https://ccbeacademyportal-backend.onrender.com`
    *(Make sure this URL matches your actual running backend URL exactly)*

### 3. Deploy
Click **Create Static Site**.

---

**Why these settings?**
*   **Build Command:** Installs your dependencies (`npm install`) and creates the optimized production build (`npm run build`).
*   **Publish Directory:** React's default build output folder is `build`, so Render needs to serve files from there.
*   **REACT_APP_API_URL:** Your frontend code uses this variable to know where to send API requests (like fetching news, events, or submitting forms). Without it, it won't connect to your database.

**Note on Free Tier:**
Render's free static sites are excellent. They have automatic HTTPS and CDN. The only limitation is bandwidth (100GB/month), which is plenty for a college portal. Your backend might sleep after inactivity, but the static frontend will always be fast and available.
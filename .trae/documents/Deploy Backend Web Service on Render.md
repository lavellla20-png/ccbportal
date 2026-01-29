To deploy your **Backend Web Service** (Django) on Render, fill out the form with these exact details.

### 1. Configuration Settings

*   **Name:** `ccb-eacademy-backend` (or similar)
*   **Repository:** `lavellla20-png/ccbportal`
*   **Language:** **Python 3** (Do **NOT** select Node)
*   **Branch:** `main`
*   **Region:** **Oregon (US West)** (It is crucial to match the region of your database for internal connection speed and free internal traffic).
*   **Root Directory:** `.` (Leave empty)
*   **Build Command:** `./build.sh`
*   **Start Command:** `gunicorn ccb_portal_backend.wsgi:application`

### 2. Environment Variables (Critical)
You must add all the variables we discussed previously. Without these, the backend will fail to start or connect to the database.

*   `DATABASE_URL`: (The PostgreSQL Internal URL you copied earlier)
*   `SECRET_KEY`: (Copy from old backend or generate new)
*   `ALLOWED_HOSTS`: `*` (or your specific backend domain)
*   `CORS_ALLOWED_ORIGINS`: `https://ccb-eacademy.onrender.com` (Your **actual** running frontend URL)
*   `PYTHON_VERSION`: `3.11.6` (or `3.13.0`)
*   `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`: (Copy from old backend)
*   `BREVO_API_KEY`: (Copy from old backend)
*   `DJANGO_SETTINGS_MODULE`: `ccb_portal_backend.production_settings`

### 3. Deploy
Click **Create Web Service**.

---

**Why these settings?**
*   **Language:** Your backend is Python/Django, not Node.js.
*   **Build Command (`./build.sh`):** This script (already in your repo) installs Python dependencies, collects static files, and runs database migrations automatically.
*   **Start Command (`gunicorn ...`):** This launches the production-grade web server for Django.
*   **Region:** Keeping the Web Service and Database in the same region (Oregon) prevents connection errors and latency.
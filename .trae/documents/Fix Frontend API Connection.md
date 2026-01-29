I have identified the issue. Your frontend was trying to connect to `/api` (a relative path), which only works if the frontend and backend are on the **same** domain. On Render, they are on **different** domains (`frontend.onrender.com` vs `backend.onrender.com`).

**The Fix:**
I have updated your `services/api.js` file to use the full URL of your backend.

1. It now looks for `process.env.REACT_APP_API_URL`.
2. If that is missing, it falls back to `https://ccbeacademyportal-backend.onrender.com/api`.

**Next Steps (Automatic):**

1. I will push this change to GitHub.
2. Render will detect the change and automatically redeploy your frontend.

**Action Required from You:**

* Ensure you have added `REACT_APP_API_URL` = `https://ccbeacademyportal-backend.onrender.com/api` (ensure `/api` is at the end if your endpoints expect it, or just the base URL if your code handles the slash) to your **Frontend** Environment Variables on Render.

* Wait for the redeploy to finish. The "News" and other dynamic content should then appear.


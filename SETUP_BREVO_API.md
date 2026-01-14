# BREVO API Key Setup

## ✅ API Key Configured

Your BREVO API key has been set up. Here's what was done:

### 1. Environment Variable Set (Current Session)
The API key has been set for your current PowerShell session.

### 2. Settings Updated
- Added `python-dotenv` support to load `.env` file automatically
- Updated `settings.py` to load environment variables from `.env` file

### 3. Next Steps

**Option A: Create .env File (Recommended for Development)**

Create a file named `.env` in your project root (`C:\CodingProjects\ccbwebmain\.env`) with this content:

```env
BREVO_API_KEY=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
DEFAULT_FROM_EMAIL=citycollegeofbayawan@gmail.com
SERVER_EMAIL=citycollegeofbayawan@gmail.com
CONTACT_INBOX=citycollegeofbayawan@gmail.com
PUBLIC_BASE_URL=http://localhost:8000
```

**Option B: Set Environment Variable Permanently (Windows)**

1. Open System Properties:
   - Press `Win + R`
   - Type `sysdm.cpl` and press Enter
   - Go to "Advanced" tab
   - Click "Environment Variables"

2. Under "User variables", click "New":
   - Variable name: `BREVO_API_KEY`
   - Variable value: `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`
   - Click OK

3. Restart your terminal/Django server

**Option C: Set in PowerShell Profile (Persistent)**

Add to your PowerShell profile:
```powershell
$env:BREVO_API_KEY="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"
```

### 4. Install python-dotenv (if using .env file)

```bash
pip install python-dotenv
```

### 5. Restart Django Server

After setting up, restart your Django server:
```bash
python manage.py runserver
```

## Testing

Try submitting the contact form again. The email should now send successfully!

## Security Note

⚠️ **IMPORTANT**: The `.env` file is already in `.gitignore` and will NOT be committed to Git. Your API key is safe.

## Troubleshooting

If emails still don't send:
1. Verify the API key is correct in BREVO dashboard
2. Check that `python-dotenv` is installed: `pip install python-dotenv`
3. Restart Django server after setting environment variable
4. Check Django logs for detailed error messages


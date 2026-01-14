# PowerShell script to set BREVO API key
# Usage: .\set_brevo_key.ps1 "your-api-key-here"

param(
    [Parameter(Mandatory=$true)]
    [string]$ApiKey
)

# Set the environment variable for current session
$env:BREVO_API_KEY = $ApiKey

# Verify it's set
Write-Host "BREVO_API_KEY has been set!" -ForegroundColor Green
Write-Host "Value: $($env:BREVO_API_KEY.Substring(0, [Math]::Min(10, $env:BREVO_API_KEY.Length)))..." -ForegroundColor Gray

Write-Host "`nTo make this permanent, add it to your system environment variables." -ForegroundColor Yellow
Write-Host "Or run this script before starting Django server each time." -ForegroundColor Yellow


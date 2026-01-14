@echo off
REM Batch script to set BREVO API key
REM Usage: set_brevo_key.bat your-api-key-here

if "%1"=="" (
    echo Error: Please provide the BREVO API key as an argument
    echo Usage: set_brevo_key.bat your-api-key-here
    exit /b 1
)

set BREVO_API_KEY=%1
echo BREVO_API_KEY has been set!
echo.
echo To use this in your current session, run:
echo   set BREVO_API_KEY=%1
echo.
echo Then start your Django server in the same command prompt window.


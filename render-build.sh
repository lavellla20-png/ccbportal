#!/usr/bin/env bash
# Render.com build script

set -o errexit  # Exit on error

echo "=== Starting Render Build Process ==="

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Build React frontend
echo "Building React frontend..."
npm run build

# Collect static files
echo "Collecting Django static files..."
python manage.py collectstatic --noinput

echo "=== Build completed successfully! ==="


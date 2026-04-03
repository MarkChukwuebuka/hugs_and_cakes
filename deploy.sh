#!/bin/bash
set -e

echo "🚀 Starting deployment..."

# Navigate to project directory
cd /var/www/hugs_and_cakes

# Pull latest changes
echo "📥 Pulling latest code..."
git pull origin main

# Install/update dependencies with uv
echo "📦 Installing dependencies..."
uv sync

# Collect static files
echo "🎨 Collecting static files..."
uv run python manage.py collectstatic --noinput

# Run migrations
echo "🗄️  Running database migrations..."
uv run python manage.py makemigrations --noinput
uv run python manage.py migrate --noinput

# Restart application
echo "🔄 Restarting application..."
sudo systemctl restart hugs_and_cakes

echo "✅ Deployment complete!"
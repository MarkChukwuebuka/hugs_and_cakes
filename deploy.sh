#!/bin/bash
set -e

echo "🚀 Starting deployment..."

APP_DIR=/var/www/hugs_and_cakes
VENV_DIR=$APP_DIR/venv

# Navigate to project directory
cd $APP_DIR

# Pull latest changes
echo "📥 Pulling latest code..."
git pull origin main

echo "📥 activate virtual env..."
source $VENV_DIR/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "🎨 Collecting static files..."
#python manage.py collectstatic --noinput

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Restart application
echo "🔄 Restarting application..."
sudo systemctl restart hugs_and_cakes

echo "✅ Deployment complete!"
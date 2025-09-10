#!/bin/bash
# Development setup script

echo "Setting up SmarTanom Backend for development..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating environment file..."
    cp .env.local .env
    echo "Please edit .env file with your configuration"
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Creating superuser...')
    exec(open('core/management/commands/create_superuser.py').read())
"

# Load sample data
echo "Loading sample data..."
python manage.py seed_data

echo "Development setup complete!"
echo "Run 'python manage.py runserver' to start the development server"

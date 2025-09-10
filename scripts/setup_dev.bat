@echo off
REM Development setup script for Windows

echo Setting up SmarTanom Backend for development...

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Copy environment file if it doesn't exist
if not exist ".env" (
    echo Creating environment file...
    copy .env.local .env
    echo Please edit .env file with your configuration
)

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Create superuser if it doesn't exist
echo Creating superuser...
python manage.py create_superuser

REM Load sample data
echo Loading sample data...
python manage.py seed_data

echo Development setup complete!
echo Run 'python manage.py runserver' to start the development server
pause

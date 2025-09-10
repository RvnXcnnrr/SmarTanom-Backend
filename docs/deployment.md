# Deployment Guide

## Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- Nginx (for production)
- SSL Certificate (for production)

## Environment Setup

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd SmarTanom-Backend
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Copy the appropriate environment file:
```bash
# For development
cp .env.local .env

# For production
cp .env.production .env
```

Edit `.env` with your actual values.

### 5. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py seed_data
```

## Development Deployment

### 1. Run Development Server
```bash
python manage.py runserver
```

### 2. Access Application
- API: http://127.0.0.1:8000/api/
- Admin: http://127.0.0.1:8000/admin/
- WebSocket Test: http://127.0.0.1:8000/websocket-test/

## Production Deployment

### 1. Server Setup (Ubuntu/Debian)
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib redis-server nginx -y

# Install supervisor for process management
sudo apt install supervisor -y
```

### 2. Database Setup
```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE smartanom_db;
CREATE USER smartanom_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE smartanom_db TO smartanom_user;
\q
```

### 3. Application Setup
```bash
# Create application directory
sudo mkdir -p /var/www/smartanom
sudo chown $USER:$USER /var/www/smartanom

# Copy application files
cp -r . /var/www/smartanom/

# Set up virtual environment
cd /var/www/smartanom
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.production .env
# Edit .env with production values

# Run migrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 4. Supervisor Configuration
Create `/etc/supervisor/conf.d/smartanom.conf`:
```ini
[program:smartanom]
command=/var/www/smartanom/.venv/bin/daphne -b 0.0.0.0 -p 8000 smartanom_backend.asgi:application
directory=/var/www/smartanom
user=www-data
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/smartanom.log
stderr_logfile=/var/log/supervisor/smartanom.log
environment=PATH="/var/www/smartanom/.venv/bin"
```

### 5. Nginx Configuration
Create `/etc/nginx/sites-available/smartanom`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/smartanom/staticfiles/;
    }

    location /media/ {
        alias /var/www/smartanom/media/;
    }
}
```

### 6. Enable and Start Services
```bash
# Enable nginx site
sudo ln -s /etc/nginx/sites-available/smartanom /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Start supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start smartanom

# Enable services to start on boot
sudo systemctl enable nginx
sudo systemctl enable supervisor
sudo systemctl enable postgresql
sudo systemctl enable redis-server
```

## Monitoring and Maintenance

### 1. Log Files
- Application logs: `/var/log/supervisor/smartanom.log`
- Nginx logs: `/var/log/nginx/access.log` and `/var/log/nginx/error.log`
- Database logs: `/var/log/postgresql/`

### 2. Health Checks
```bash
# Check application status
sudo supervisorctl status smartanom

# Check nginx status
sudo systemctl status nginx

# Check database connection
python manage.py dbshell

# Check Redis connection
redis-cli ping
```

### 3. Updates
```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application
sudo supervisorctl restart smartanom
```

## Security Considerations

1. **Environment Variables**: Never commit `.env` files
2. **Database Security**: Use strong passwords and limit access
3. **SSL/TLS**: Always use HTTPS in production
4. **Firewall**: Configure UFW or iptables
5. **Regular Updates**: Keep system and dependencies updated
6. **Backup Strategy**: Regular database and media backups

## Troubleshooting

### Common Issues
1. **502 Bad Gateway**: Check if the application is running
2. **WebSocket Connection Failed**: Check nginx WebSocket configuration
3. **Database Connection Error**: Verify database credentials and service status
4. **Static Files Not Loading**: Run `collectstatic` and check nginx configuration

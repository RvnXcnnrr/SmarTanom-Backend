#!/bin/bash
# Backup script for production

BACKUP_DIR="/var/backups/smartanom"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_NAME="smartanom_db"
DB_USER="smartanom_user"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

echo "Starting backup process..."

# Database backup
echo "Backing up database..."
pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_DIR/db_backup_$TIMESTAMP.sql

# Media files backup
echo "Backing up media files..."
tar -czf $BACKUP_DIR/media_backup_$TIMESTAMP.tar.gz /var/www/smartanom/media/

# Application files backup (optional)
echo "Backing up application files..."
tar -czf $BACKUP_DIR/app_backup_$TIMESTAMP.tar.gz /var/www/smartanom/ --exclude=.venv --exclude=media --exclude=staticfiles --exclude=__pycache__

# Clean old backups (keep last 7 days)
echo "Cleaning old backups..."
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed successfully!"
echo "Files created:"
ls -la $BACKUP_DIR/*$TIMESTAMP*

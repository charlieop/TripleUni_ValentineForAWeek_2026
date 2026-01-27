# Docker Deployment Guide

This guide covers how to build, run, and manage the Django application using Docker.

## Prerequisites

- Docker and Docker Compose installed on your Ubuntu server
- Nginx configured (see nginx configuration section below)
- SECRETS.json file in the backend directory

## Directory Structure

The following directories/files are mounted from the host to persist data:
- `db.sqlite3` - SQLite database
- `media/` - User uploaded files
- `logs/` - Application logs
- `static/` - Static files (CSS, JS, images)

Make sure these exist before running:

```bash
cd /path/to/backend
mkdir -p media logs static
touch db.sqlite3
```

## Build and Run

### Initial Setup

1. **Build the Docker image:**
   ```bash
   cd /path/to/backend
   docker compose build
   ```

2. **Start the container:**
   ```bash
   docker compose up -d
   ```

   The container will:
   - Run migrations automatically
   - Collect static files
   - Start gunicorn on port 8000

3. **Check if it's running:**
   ```bash
   docker compose ps
   docker compose logs -f
   ```

### Create Django Superuser

```bash
docker compose exec django python manage.py createsuperuser
```

## Managing the Container

### Start the container
```bash
docker compose start
```

### Stop the container
```bash
docker compose stop
```

### Restart the container (after code updates)
```bash
docker compose restart
```

### View logs
```bash
# Follow logs in real-time
docker compose logs -f

# View last 100 lines
docker compose logs --tail=100

# View logs for specific service
docker compose logs -f django
```

### Rebuild after dependency changes
If you update `requirements.txt`:
```bash
docker compose down
docker compose build --no-cache
docker compose up -d
sudo docker compose exec django chown -R www-data:www-data /app/static

cd /home/ubuntu/TripleUni_ValentineForAWeek_2026/backend
sudo chown -R www-data:www-data static
sudo chmod -R 755 static
sudo find static -type f -exec chmod 644 {} \;
```

## After Code Updates

When you update your code in the project folder:

### Option 1: Quick restart (for Python code changes)
```bash
docker compose restart
```

### Option 2: Full rebuild (for dependency or Dockerfile changes)
```bash
docker compose down
docker compose build
docker compose up -d
```

## Running Django Management Commands

Execute any Django management command inside the container:

```bash
# Run migrations
docker compose exec django python manage.py migrate

# Create superuser
docker compose exec django python manage.py createsuperuser

# Collect static files
docker compose exec django python manage.py collectstatic --noinput

# Open Django shell
docker compose exec django python manage.py shell

# Run custom commands
docker compose exec django python manage.py <your_command>
```

## Accessing the Container Shell

```bash
docker compose exec django bash
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker compose logs

# Check if port 8000 is already in use
sudo netstat -tlnp | grep 8000
```

### Permission issues with mounted volumes
```bash
# Fix ownership (run on host)
sudo chown -R $USER:$USER media logs db.sqlite3
```

### Database is locked
This can happen if the SQLite database is accessed by multiple processes:
```bash
docker compose restart
```

### Static files not updating
```bash
docker compose exec django python manage.py collectstatic --noinput --clear
```

## Complete Cleanup

To completely remove the container and image:

```bash
docker compose down
docker rmi valentine_django
```

**Note:** This does NOT delete your data (db.sqlite3, media, logs) as they're stored on the host.

## Nginx Configuration

See the main README for the complete nginx configuration that serves static and media files directly.

## Auto-restart on Server Reboot

The container is configured with `restart: unless-stopped`, which means it will automatically start when the server reboots.

To check the restart policy:
```bash
docker inspect valentine_django | grep RestartPolicy -A 3
```

## Monitoring

### Check container resource usage
```bash
docker stats valentine_django
```

### Check container health
```bash
docker compose ps
```

### Access logs location
- Application logs: `./logs/access.log` and `./logs/error.log`
- Docker logs: `docker compose logs`

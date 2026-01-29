FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .

# Create directories for volumes (will be mounted from host)
RUN mkdir -p /app/media /app/logs /app/static
RUN touch /app/db.sqlite3

RUN chown -R www-data:www-data /app/media /app/logs /app/static
RUN chmod -R 755 /app/media /app/logs /app/static
RUN chown www-data:www-data /app/db.sqlite3
RUN chmod 664 /app/db.sqlite3

# Collect static files
RUN python manage.py collectstatic --noinput

# make migrations
RUN python manage.py makemigrations --noinput
RUN python manage.py migrate --noinput

EXPOSE 8000

# Use gunicorn with access log to logs folder
CMD ["gunicorn", "server.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "5", \
     "--timeout", "300", \
     "--access-logfile", "/app/logs/access.log", \
     "--error-logfile", "/app/logs/error.log", \
     "--log-level", "info"]

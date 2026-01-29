import os

from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

app = Celery("server")

# Read CELERY_ settings from Django settings with the CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks.py in installed apps
app.autodiscover_tasks()

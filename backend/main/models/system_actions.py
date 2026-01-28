from django.db import models
from .config import Config


class SystemActions(Config):
    """
    Proxy model for System Actions page in Django admin.
    This allows us to create a separate admin interface for system actions
    without creating a new database table.
    """

    class Meta:
        proxy = True
        verbose_name = "系统操作"
        verbose_name_plural = "系统操作"
        app_label = "main"

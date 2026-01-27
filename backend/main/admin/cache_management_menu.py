"""
Register cache management menu item in Django admin.
This file is imported in admin/__init__.py to ensure the menu is registered.
"""

from django.urls import reverse
from django.utils.html import format_html


def add_cache_management_to_menu(request, context):
    """Add cache management link to admin menu context."""
    if hasattr(context, "available_apps"):
        # Find or create a custom section for system tools
        cache_url = reverse("admin:cache_management")
        cache_link = format_html(
            '<a href="{}" class="admin-menu-link">Cache Management</a>', cache_url
        )
        # This will be handled by Unfold's menu system
        return cache_link
    return None

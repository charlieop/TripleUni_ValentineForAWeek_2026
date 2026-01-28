from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.utils.html import format_html
from django.contrib import messages
from django.forms.models import model_to_dict
from django.db import models
import pickle
import json


def get_all_cache_keys():
    """
    Get all cache keys from the cache backend.
    For LocMemCache, we need to access the internal _cache dict.
    Keys are stored with version prefix (e.g., :1:key), so we strip it.
    """
    try:
        raw_keys = []
        # Access the internal cache storage
        if hasattr(cache, "_cache"):
            # LocMemCache stores keys in _cache dict
            # _cache is a dict-like object, get all keys
            raw_keys = list(cache._cache.keys())
        elif hasattr(cache, "_expire_info"):
            # Alternative LocMemCache structure
            if hasattr(cache, "_cache"):
                raw_keys = list(cache._cache.keys())
        elif hasattr(cache, "keys"):
            # Some cache backends have a keys() method (like Redis with django-redis)
            try:
                raw_keys = cache.keys("*")
            except:
                pass
        elif hasattr(cache, "get_backend"):
            # Try to access the backend directly
            backend = cache.get_backend()
            if hasattr(backend, "_cache"):
                raw_keys = list(backend._cache.keys())

        # Strip version prefix from keys (format: :VERSION:key)
        # LocMemCache stores keys with version prefix like :1:key
        stripped_keys = []
        for key in raw_keys:
            # Check if key has version prefix pattern :VERSION:
            if isinstance(key, str) and ":" in key:
                # Find the second colon (after version number)
                parts = key.split(":", 2)
                if len(parts) >= 3 and parts[0] == "" and parts[1].isdigit():
                    # Strip the :VERSION: prefix
                    stripped_key = parts[2] if len(parts) > 2 else key
                    stripped_keys.append(stripped_key)
                else:
                    # No version prefix, use as is
                    stripped_keys.append(key)
            else:
                stripped_keys.append(key)

        return stripped_keys
    except Exception as e:
        # Log the error but don't crash
        import logging

        logger = logging.getLogger(__name__)
        logger.warning(f"Could not retrieve cache keys: {str(e)}")
        return []


def parse_cache_structure(keys, prefix=""):
    """
    Parse cache keys into a file-system-like structure.
    Returns a dict with 'directories' and 'keys' lists.

    Example:
    - Keys: ['a:b', 'a:c:d', 'a:c:e']
    - Prefix: 'a:'
    - Returns: {
        'directories': ['c'],
        'keys': ['b']
      }
    """
    directories = set()
    leaf_keys = []

    prefix_len = len(prefix) if prefix else 0

    for key in keys:
        if not key.startswith(prefix):
            continue

        remaining = key[prefix_len:]
        if not remaining:
            continue

        # Split by colon to get the next level
        parts = remaining.split(":", 1)

        if len(parts) == 1:
            # This is a leaf key (no more colons)
            leaf_keys.append(key)
        else:
            # This is a directory (has more levels)
            dir_name = parts[0]
            directories.add(dir_name)

    return {"directories": sorted(list(directories)), "keys": sorted(leaf_keys)}


def get_cache_value(key):
    """Get and format cache value for display."""
    try:
        value = cache.get(key)
        if value is None:
            return None, "Key not found or expired"

        # Try to format the value
        try:
            # Check if value is a Django model instance
            if isinstance(value, models.Model):
                # Convert model to dictionary with all field values
                model_dict = model_to_dict(value)
                # Add model metadata
                model_info = {
                    "model": f"{value._meta.app_label}.{value._meta.model_name}",
                    "pk": str(value.pk),
                    "fields": model_dict,
                }
                formatted = json.dumps(
                    model_info, indent=2, ensure_ascii=False, default=str
                )
            elif isinstance(value, (dict, list)):
                formatted = json.dumps(value, indent=2, ensure_ascii=False, default=str)
            elif isinstance(value, str):
                formatted = value
            else:
                formatted = str(value)
            return value, formatted
        except Exception:
            return value, str(value)
    except Exception as e:
        return None, f"Error: {str(e)}"


@staff_member_required
def cache_management_view(request):
    """Main cache management view."""
    # Only allow superusers
    if not request.user.is_superuser:
        from django.contrib.auth.decorators import user_passes_test
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied

    # Default to empty path (root level) if not specified
    current_path = request.GET.get("path", "").strip()

    # Handle actions
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "delete_key":
            key = request.POST.get("key")
            if key:
                try:
                    cache.delete(key)
                    messages.success(
                        request, f'Cache key "{key}" deleted successfully.'
                    )
                except Exception as e:
                    messages.error(request, f"Error deleting key: {str(e)}")
            return redirect(f"{reverse('admin:cache_management')}?path={current_path}")

        elif action == "flush_all":
            try:
                cache.clear()
                messages.success(request, "All cache cleared successfully.")
            except Exception as e:
                messages.error(request, f"Error clearing cache: {str(e)}")
            return redirect(reverse("admin:cache_management"))

    # Get all cache keys
    all_keys = get_all_cache_keys()

    # Parse structure for current path
    structure = parse_cache_structure(all_keys, current_path)

    # Get parent path (go up one level)
    parent_path = ""
    if current_path:
        parts = current_path.rstrip(":").split(":")
        if len(parts) > 1:
            parent_path = ":".join(parts[:-1]) + ":"
        else:
            parent_path = ""

    # Get cache values for leaf keys (limit to first 50 for performance)
    cache_items = []
    for key in structure["keys"][:50]:
        value, formatted_value = get_cache_value(key)
        cache_items.append(
            {
                "key": key,
                "value": value,
                "formatted_value": formatted_value,
                "has_more": len(structure["keys"]) > 50,
            }
        )

    # Check if there are more keys
    has_more_keys = len(structure["keys"]) > 50

    # Get app config for template compatibility
    from django.apps import apps

    try:
        app_config = apps.get_app_config("main")
    except LookupError:
        app_config = None

    # Create a minimal opts object that won't trigger URL generation
    # We'll use a real model's opts to avoid URL reverse errors
    from ..models import Config

    real_opts = Config._meta

    context = {
        "title": "Cache Management",
        "current_path": current_path,
        "parent_path": parent_path,
        "directories": structure["directories"],
        "cache_items": cache_items,
        "has_more_keys": has_more_keys,
        "total_keys_shown": len(cache_items),
        "total_directories": len(structure["directories"]),
        "opts": real_opts,  # Use a real model's opts to avoid URL issues
        "has_permission": True,
        "site_header": admin.site.site_header,
        "site_title": admin.site.site_title,
    }

    return render(request, "admin/cache_management.html", context)


@staff_member_required
@require_http_methods(["GET"])
def cache_key_detail_view(request):
    """Get detailed information about a specific cache key."""
    # Only allow superusers
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied

    key = request.GET.get("key")
    if not key:
        return JsonResponse({"error": "Key parameter required"}, status=400)

    value, formatted_value = get_cache_value(key)

    if value is None:
        return JsonResponse({"key": key, "exists": False, "message": formatted_value})

    # Check if it's a Django model for additional info
    is_model = isinstance(value, models.Model)
    model_info = None
    if is_model:
        model_info = {
            "app_label": value._meta.app_label,
            "model_name": value._meta.model_name,
            "pk": str(value.pk),
        }

    return JsonResponse(
        {
            "key": key,
            "exists": True,
            "value": formatted_value,
            "type": type(value).__name__,
            "is_django_model": is_model,
            "model_info": model_info,
        }
    )


# Register URLs by monkey-patching admin site's get_urls
_original_get_urls = admin.site.get_urls


def get_urls_with_cache_management():
    """Extend admin URLs with cache management."""
    from django.urls import path

    urls = _original_get_urls()
    # Insert cache management URLs before other admin URLs
    urls.insert(
        0,
        path(
            "cache-management/",
            admin.site.admin_view(cache_management_view),
            name="cache_management",
        ),
    )
    urls.insert(
        1,
        path(
            "cache-management/detail/",
            admin.site.admin_view(cache_key_detail_view),
            name="cache_key_detail",
        ),
    )
    return urls


# Only patch if not already patched
if not hasattr(admin.site, "_cache_management_patched"):
    admin.site.get_urls = get_urls_with_cache_management
    admin.site._cache_management_patched = True

from django.contrib import admin
from django.shortcuts import render
from django.urls import reverse
from unfold.admin import ModelAdmin

from ..models import SystemActions


@admin.register(SystemActions)
class SystemActionsAdmin(ModelAdmin):
    """Admin interface for System Actions page."""

    def has_module_permission(self, request):
        """Only superadmin can see this module."""
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        """Only superadmin can view system actions."""
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        """Disable change permission - this is just a navigation page."""
        return False

    def has_add_permission(self, request):
        """Disable add permission - this is just a navigation page."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable delete permission - this is just a navigation page."""
        return False

    def changelist_view(self, request, extra_context=None):
        """Override changelist to show system actions page."""
        context = {
            **self.admin_site.each_context(request),
            "title": "系统操作",
            "opts": self.model._meta,
            "has_view_permission": self.has_view_permission(request),
            "cache_management_url": reverse("admin:cache_management"),
        }
        return render(request, "admin/system_actions.html", context)

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.urls import reverse, path
from django.contrib import messages
from unfold.admin import ModelAdmin

from ..models import SystemActions
from ..mixin import UtilMixin


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
            "calculate_rank_url": reverse("admin:calculate_rank"),
        }
        return render(request, "admin/system_actions.html", context)


@staff_member_required
def calculate_rank_view(request):
    """View to calculate and cache match rankings."""
    # Only allow superusers
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    # Only handle POST requests
    if request.method != "POST":
        return redirect(reverse("admin:main_systemactions_changelist"))

    # Create a dummy class with UtilMixin to call calculate_rank
    class DummyView(UtilMixin):
        pass

    dummy_view = DummyView()
    try:
        ranking_dict = dummy_view.calculate_rank()
        total_matches = len(ranking_dict)
        messages.success(
            request,
            f"排名计算成功！共计算了 {total_matches} 个匹配的排名。"
        )
    except Exception as e:
        messages.error(request, f"计算排名时出错: {str(e)}")

    return redirect(reverse("admin:main_systemactions_changelist"))


# Register URL by monkey-patching admin site's get_urls
# Check if cache_management already patched it
if hasattr(admin.site, "_cache_management_patched"):
    # Use the existing patched version
    _original_get_urls_for_rank = admin.site.get_urls
else:
    # Use the original if not patched yet
    _original_get_urls_for_rank = admin.site.get_urls


def get_urls_with_calculate_rank():
    """Extend admin URLs with calculate rank action."""
    urls = _original_get_urls_for_rank()
    # Insert calculate rank URL before other admin URLs
    urls.insert(
        0,
        path(
            "calculate-rank/",
            admin.site.admin_view(calculate_rank_view),
            name="calculate_rank",
        ),
    )
    return urls


# Only patch if not already patched
if not hasattr(admin.site, "_calculate_rank_patched"):
    admin.site.get_urls = get_urls_with_calculate_rank
    admin.site._calculate_rank_patched = True

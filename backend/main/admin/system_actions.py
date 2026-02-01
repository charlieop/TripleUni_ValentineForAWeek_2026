from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.urls import reverse, path
from django.contrib import messages
from unfold.admin import ModelAdmin

from ..models import SystemActions
from ..mixin import UtilMixin
from ..logger import CustomLogger
from ..utils import (
    remind_payment_to_not_paid_applicants,
    notify_first_match_result_to_all,
    notify_first_match_result_to_not_confirmed_applicants,
    notify_second_match_result_to_all,
    notify_activity_start_to_all,
    notify_daily_task_deadline_to_all,
    notify_exit_questionnaire_deadline_to_all,
)

logger = CustomLogger("system_actions")


@admin.register(SystemActions)
class SystemActionsAdmin(ModelAdmin):
    """Admin interface for System Actions page."""

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
            "remind_payment_url": reverse("admin:remind_payment"),
            "notify_first_match_all_url": reverse("admin:notify_first_match_all"),
            "notify_first_match_confirm_url": reverse(
                "admin:notify_first_match_confirm"
            ),
            "notify_second_match_url": reverse("admin:notify_second_match"),
            "notify_activity_start_url": reverse("admin:notify_activity_start"),
            "notify_daily_task_url": reverse("admin:notify_daily_task"),
            "notify_exit_questionnaire_url": reverse("admin:notify_exit_questionnaire"),
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
            request, f"排名计算成功！共计算了 {total_matches} 个匹配的排名。"
        )
        logger.info(
            f"{request.user.username} calculated rank successfully for {total_matches} matches"
        )
    except Exception as e:
        messages.error(request, f"计算排名时出错: {str(e)}")
        logger.error(f"{request.user.username} calculated rank failed: {str(e)}")
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


@staff_member_required
def remind_payment_view(request):
    """View to remind payment to not paid applicants."""
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied

    if request.method != "POST":
        return redirect(reverse("admin:main_systemactions_changelist"))

    # Check for confirmation
    if request.POST.get("confirmed") != "true":
        messages.warning(request, "操作已取消")
        return redirect(reverse("admin:main_systemactions_changelist"))

    try:
        success = remind_payment_to_not_paid_applicants()
        if success:
            messages.success(request, "押金支付提醒通知发送成功！")
            logger.info(
                f"{request.user.username} sent payment reminder notification successfully"
            )
        else:
            messages.error(request, "押金支付提醒通知发送失败，请查看日志")
            logger.error(
                f"{request.user.username} sent payment reminder notification failed"
            )
    except Exception as e:
        messages.error(request, f"发送通知时出错: {str(e)}")
        logger.error(
            f"{request.user.username} sent payment reminder notification error: {str(e)}"
        )

    return redirect(reverse("admin:main_systemactions_changelist"))


@staff_member_required
def notify_first_match_all_view(request):
    """View to notify first match result to all applicants."""
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied

    if request.method != "POST":
        return redirect(reverse("admin:main_systemactions_changelist"))

    if request.POST.get("confirmed") != "true":
        messages.warning(request, "操作已取消")
        return redirect(reverse("admin:main_systemactions_changelist"))

    try:
        success = notify_first_match_result_to_all()
        if success:
            messages.success(request, "第一轮匹配结果通知发送成功！")
            logger.info(
                f"{request.user.username} sent first match result notification successfully"
            )
        else:
            messages.error(request, "第一轮匹配结果通知发送失败，请查看日志")
            logger.error(
                f"{request.user.username} sent first match result notification failed"
            )
    except Exception as e:
        messages.error(request, f"发送通知时出错: {str(e)}")
        logger.error(
            f"{request.user.username} sent first match result notification error: {str(e)}"
        )

    return redirect(reverse("admin:main_systemactions_changelist"))


@staff_member_required
def notify_first_match_confirm_view(request):
    """View to notify first match confirm reminder to not confirmed applicants."""
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied

    if request.method != "POST":
        return redirect(reverse("admin:main_systemactions_changelist"))

    if request.POST.get("confirmed") != "true":
        messages.warning(request, "操作已取消")
        return redirect(reverse("admin:main_systemactions_changelist"))

    try:
        success = notify_first_match_result_to_not_confirmed_applicants()
        if success:
            messages.success(request, "第一轮确认提醒通知发送成功！")
            logger.info(
                f"{request.user.username} sent first match confirm reminder notification successfully"
            )
        else:
            messages.error(request, "第一轮确认提醒通知发送失败，请查看日志")
            logger.error(
                f"{request.user.username} sent first match confirm reminder notification failed"
            )
    except Exception as e:
        messages.error(request, f"发送通知时出错: {str(e)}")
        logger.error(
            f"{request.user.username} sent first match confirm reminder notification error: {str(e)}"
        )

    return redirect(reverse("admin:main_systemactions_changelist"))


@staff_member_required
def notify_second_match_view(request):
    """View to notify second match result to all applicants."""
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied

    if request.method != "POST":
        return redirect(reverse("admin:main_systemactions_changelist"))

    if request.POST.get("confirmed") != "true":
        messages.warning(request, "操作已取消")
        return redirect(reverse("admin:main_systemactions_changelist"))

    try:
        success = notify_second_match_result_to_all()
        if success:
            messages.success(request, "第二轮匹配结果通知发送成功！")
            logger.info(
                f"{request.user.username} sent second match result notification successfully"
            )
        else:
            messages.error(request, "第二轮匹配结果通知发送失败，请查看日志")
            logger.error(
                f"{request.user.username} sent second match result notification failed"
            )
    except Exception as e:
        messages.error(request, f"发送通知时出错: {str(e)}")
        logger.error(
            f"{request.user.username} sent second match result notification error: {str(e)}"
        )

    return redirect(reverse("admin:main_systemactions_changelist"))


@staff_member_required
def notify_activity_start_view(request):
    """View to notify activity start to all applicants."""
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied

    if request.method != "POST":
        return redirect(reverse("admin:main_systemactions_changelist"))

    if request.POST.get("confirmed") != "true":
        messages.warning(request, "操作已取消")
        return redirect(reverse("admin:main_systemactions_changelist"))

    try:
        success = notify_activity_start_to_all()
        if success:
            messages.success(request, "活动开始通知发送成功！")
            logger.info(
                f"{request.user.username} sent activity start notification successfully"
            )
        else:
            messages.error(request, "活动开始通知发送失败，请查看日志")
            logger.error(
                f"{request.user.username} sent activity start notification failed"
            )
    except Exception as e:
        messages.error(request, f"发送通知时出错: {str(e)}")
        logger.error(
            f"{request.user.username} sent activity start notification error: {str(e)}"
        )

    return redirect(reverse("admin:main_systemactions_changelist"))


@staff_member_required
def notify_daily_task_view(request):
    """View to notify daily task deadline to all applicants."""
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied

    if request.method != "POST":
        return redirect(reverse("admin:main_systemactions_changelist"))

    if request.POST.get("confirmed") != "true":
        messages.warning(request, "操作已取消")
        return redirect(reverse("admin:main_systemactions_changelist"))

    day = request.POST.get("day")
    if not day:
        messages.error(request, "请选择天数（1-7）")
        return redirect(reverse("admin:main_systemactions_changelist"))

    try:
        day = int(day)
        if day < 1 or day > 7:
            messages.error(request, "天数必须在1-7之间")
            return redirect(reverse("admin:main_systemactions_changelist"))
    except ValueError:
        messages.error(request, "无效的天数")
        return redirect(reverse("admin:main_systemactions_changelist"))

    try:
        success = notify_daily_task_deadline_to_all(day)
        if success:
            messages.success(request, f"第{day}天任务截止提醒通知发送成功！")
            logger.info(
                f"{request.user.username} sent daily task reminder notification for day {day} successfully"
            )
        else:
            messages.error(request, f"第{day}天任务截止提醒通知发送失败，请查看日志")
            logger.error(
                f"{request.user.username} sent daily task reminder notification for day {day} failed"
            )
    except Exception as e:
        messages.error(request, f"发送通知时出错: {str(e)}")
        logger.error(
            f"{request.user.username} sent daily task reminder notification error: {str(e)}"
        )

    return redirect(reverse("admin:main_systemactions_changelist"))


@staff_member_required
def notify_exit_questionnaire_view(request):
    """View to notify exit questionnaire deadline to all applicants."""
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied

    if request.method != "POST":
        return redirect(reverse("admin:main_systemactions_changelist"))

    if request.POST.get("confirmed") != "true":
        messages.warning(request, "操作已取消")
        return redirect(reverse("admin:main_systemactions_changelist"))

    try:
        success = notify_exit_questionnaire_deadline_to_all()
        if success:
            messages.success(request, "结束问卷提交截止提醒通知发送成功！")
            logger.info(
                f"{request.user.username} sent exit questionnaire reminder notification successfully"
            )
        else:
            messages.error(request, "结束问卷提交截止提醒通知发送失败，请查看日志")
            logger.error(
                f"{request.user.username} sent exit questionnaire reminder notification failed"
            )
    except Exception as e:
        messages.error(request, f"发送通知时出错: {str(e)}")
        logger.error(
            f"{request.user.username} sent exit questionnaire reminder notification error: {str(e)}"
        )

    return redirect(reverse("admin:main_systemactions_changelist"))


# Register URL by monkey-patching admin site's get_urls
# Get the current get_urls function (which may already be patched by calculate_rank)
_current_get_urls = admin.site.get_urls


def get_urls_with_notifications():
    """Extend admin URLs with notification actions."""
    urls = _current_get_urls()
    # Insert notification URLs
    notification_urls = [
        path(
            "remind-payment/",
            admin.site.admin_view(remind_payment_view),
            name="remind_payment",
        ),
        path(
            "notify-first-match-all/",
            admin.site.admin_view(notify_first_match_all_view),
            name="notify_first_match_all",
        ),
        path(
            "notify-first-match-confirm/",
            admin.site.admin_view(notify_first_match_confirm_view),
            name="notify_first_match_confirm",
        ),
        path(
            "notify-second-match/",
            admin.site.admin_view(notify_second_match_view),
            name="notify_second_match",
        ),
        path(
            "notify-activity-start/",
            admin.site.admin_view(notify_activity_start_view),
            name="notify_activity_start",
        ),
        path(
            "notify-daily-task/",
            admin.site.admin_view(notify_daily_task_view),
            name="notify_daily_task",
        ),
        path(
            "notify-exit-questionnaire/",
            admin.site.admin_view(notify_exit_questionnaire_view),
            name="notify_exit_questionnaire",
        ),
    ]
    # Insert notification URLs at the beginning (before other admin URLs)
    urls = notification_urls + urls
    return urls


# Only patch if not already patched
if not hasattr(admin.site, "_notifications_patched"):
    admin.site.get_urls = get_urls_with_notifications
    admin.site._notifications_patched = True

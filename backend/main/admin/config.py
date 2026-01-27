from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from unfold.admin import ModelAdmin

from ..models import Config


@admin.register(Config)
class ConfigAdmin(ModelAdmin):
    fieldsets = (
        (
            "系统状态",
            {
                "fields": (
                    "maintenance_mode",
                    "expected_maintenance_end",
                    "debug_mode",
                ),
                "description": "系统维护和调试设置",
            },
        ),
        (
            "时区设置",
            {
                "fields": ("timezone",),
                "description": "系统使用的时区（例如: America/New_York, Asia/Shanghai）",
            },
        ),
        (
            "申请阶段",
            {
                "fields": (
                    "application_start",
                    "application_end",
                ),
                "description": "用户提交申请的时间段",
            },
        ),
        (
            "第一轮匹配",
            {
                "fields": (
                    "first_match_result_release",
                    "first_match_confirm_end",
                ),
                "description": "第一轮匹配结果发布和确认时间",
            },
        ),
        (
            "第二轮匹配",
            {
                "fields": ("second_match_result_release",),
                "description": "第二轮匹配结果发布时间",
            },
        ),
        (
            "活动阶段",
            {
                "fields": ("activity_start",),
                "description": "活动正式开始时间",
            },
        ),
        (
            "任务阶段",
            {
                "fields": (
                    "first_mission_release",
                    "first_mission_end",
                ),
                "description": "第一天任务的发布和截止时间（其他天数自动计算）",
            },
        ),
        (
            "退出问卷",
            {
                "fields": (
                    "exit_questionnaire_release",
                    "exit_questionnaire_end",
                ),
                "description": "退出问卷的开放时间段",
            },
        ),
        (
            "元数据",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
    readonly_fields = ["created_at", "updated_at"]

    def changelist_view(self, request, extra_context=None):
        """Override changelist to redirect directly to the config entry."""
        config = Config.objects.first()
        if config:
            # If config exists, redirect to its change page
            url = reverse("admin:main_config_change", args=[config.pk])
            return redirect(url)
        else:
            # If config doesn't exist, redirect to add page
            url = reverse("admin:main_config_add")
            return redirect(url)

    def has_module_permission(self, request):
        """Only superadmin can see this module."""
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        """Only superadmin can view config."""
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        """Only superadmin can change config."""
        return request.user.is_superuser

    def has_add_permission(self, request):
        """Only superadmin can add config, and only one instance allowed."""
        return request.user.is_superuser and not Config.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of Config."""
        return False

from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from unfold.admin import ModelAdmin

from ..models import WeChatInfo


class WechatInfoHasAppliedFilter(admin.SimpleListFilter):
    title = "是否提交申请"
    parameter_name = "has_applied"

    def lookups(self, request, model_admin):
        return [
            ("True", "已提交"),
            ("False", "未提交"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(applicant__isnull=False)
        if self.value() == "False":
            return queryset.filter(applicant__isnull=True)
        return queryset


@admin.register(WeChatInfo)
class WeChatInfoAdmin(ModelAdmin):
    search_fields = ["nickname", "openid", "unionid"]
    readonly_fields = [
        "id",
        "head_image_large",
        "head_image_path",
        "created_at",
        "get_applicant_link",
    ]
    list_display = ["nickname", "head_image_tag", "get_applicant_name", "created_at"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "nickname",
                    "head_image",
                    "head_image_url",
                    "head_image_large",
                    "head_image_path",
                    "get_applicant_link",
                    "created_at",
                )
            },
        ),
    )
    ordering = ["-created_at"]
    list_filter = [WechatInfoHasAppliedFilter, "created_at"]
    date_hierarchy = "created_at"

    def get_list_display_links(self, request, list_display):
        return list_display

    def get_exclude(self, request, obj):
        return [] if request.user.is_superuser else ["openid", "unionid"]

    def get_readonly_fields(self, request, obj=None):
        """Make openid readonly when editing existing object to prevent creating duplicates."""
        readonly = list(super().get_readonly_fields(request, obj))
        if obj:  # Editing existing object - prevent openid from being changed
            readonly.append("openid")
        return readonly

    def get_fieldsets(self, request, obj):
        fieldsets = super().get_fieldsets(request, obj)
        if request.user.is_superuser:
            fieldsets += (("Additional Info", {"fields": ("id", "openid", "unionid")}),)
        return fieldsets

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("applicant")

    @admin.display(description="申请人姓名", ordering="applicant__name")
    def get_applicant_name(self, obj):
        if hasattr(obj, "applicant"):
            return obj.applicant.name
        return "-"

    @admin.display(description="申请人", ordering="applicant__name")
    def get_applicant_link(self, obj):
        if hasattr(obj, "applicant"):
            return format_html(
                '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/applicant/{}/change/">{}</a>',
                obj.applicant.id,
                obj.applicant.name,
            )

        return "-"

    @admin.display(description="头像")
    def head_image_tag(self, obj):
        # Prefer uploaded image over URL
        if obj.head_image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 4px;" />',
                obj.head_image.url,
            )
        elif obj.head_image_url:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 4px;" />',
                obj.head_image_url,
            )
        return "无头像"

    @admin.display(description="头像")
    def head_image_large(self, obj):
        # Prefer uploaded image over URL
        if obj.head_image:
            return format_html(
                '<img src="{}" width="150" height="150" style="object-fit: cover; border-radius: 4px;" />',
                obj.head_image.url,
            )
        elif obj.head_image_url:
            return format_html(
                '<img src="{}" width="150" height="150" style="object-fit: cover; border-radius: 4px;" />',
                obj.head_image_url,
            )
        return "无头像"

    @admin.display(description="存储路径")
    def head_image_path(self, obj):
        if obj.head_image:
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                obj.head_image.url,
                obj.head_image.name,
            )
        return "-"

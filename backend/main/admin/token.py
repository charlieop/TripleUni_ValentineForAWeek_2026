from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from ..models import Token


class TokenHasApplicantFilter(admin.SimpleListFilter):
    title = "是否已申请"
    parameter_name = "has_applicant"

    def lookups(self, request, model_admin):
        return [
            ("yes", "已申请"),
            ("no", "未申请"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(wechat_info__applicant__isnull=False)
        if self.value() == "no":
            return queryset.filter(wechat_info__applicant__isnull=True)
        return queryset


@admin.register(Token)
class TokenAdmin(ModelAdmin):
    list_display = [
        "get_nickname",
        "get_token_short",
        "get_has_applicant",
        "created_at",
    ]
    list_filter = [TokenHasApplicantFilter, "created_at"]
    search_fields = [
        "wechat_info__nickname",
        "wechat_info__openid",
        "token",
    ]
    readonly_fields = [
        "id",
        "token",
        "wechat_info",
        "get_wechat_link",
        "get_applicant_link",
        "created_at",
    ]
    autocomplete_fields = ["wechat_info"]
    fieldsets = (
        (
            "Token信息",
            {
                "fields": (
                    "id",
                    "token",
                    "get_wechat_link",
                    "get_applicant_link",
                )
            },
        ),
        (
            "时间戳",
            {"fields": ("created_at",)},
        ),
    )
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("wechat_info")

    @admin.display(description="微信昵称", ordering="wechat_info__nickname")
    def get_nickname(self, obj):
        return obj.wechat_info.nickname

    @admin.display(description="Token (前8位)")
    def get_token_short(self, obj):
        return str(obj.token)[:8] + "..."

    @admin.display(description="已申请", boolean=True)
    def get_has_applicant(self, obj):
        return hasattr(obj.wechat_info, "applicant")

    @admin.display(description="微信信息")
    def get_wechat_link(self, obj):
        return format_html(
            '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/wechatinfo/{}/change/">{}</a>',
            obj.wechat_info.openid,
            obj.wechat_info.nickname,
        )

    @admin.display(description="关联申请人")
    def get_applicant_link(self, obj):
        if hasattr(obj.wechat_info, "applicant"):
            applicant = obj.wechat_info.applicant
            return format_html(
                '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/applicant/{}/change/">{}</a>',
                applicant.id,
                applicant.name,
            )
        return "-"

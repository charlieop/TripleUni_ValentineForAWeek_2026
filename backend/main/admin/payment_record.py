from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from ..models import PaymentRecord


@admin.register(PaymentRecord)
class PaymentRecordAdmin(ModelAdmin):
    search_fields = [
        "applicant__name",
        "applicant__wxid",
        "applicant__wechat_info__nickname",
        "transaction_id",
        "out_trade_no",
        "handle_by",
    ]
    list_display = [
        "get_applicant_name",
        "get_applicant_school",
        "get_applicant_wxid",
        "transaction_id",
        "handle_by",
        "created_at",
    ]
    list_filter = [
        "handle_by",
    ]
    readonly_fields = [
        "id",
        "applicant",
        "get_applicant_link",
        "created_at",
    ]
    fieldsets = (
        (
            "付款信息",
            {
                "fields": (
                    "id",
                    "get_applicant_link",
                    ("transaction_id", "out_trade_no"),
                    "handle_by",
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
        return (
            super()
            .get_queryset(request)
            .select_related("applicant", "applicant__wechat_info")
        )

    def get_fields(self, request, obj):
        return (
            [
                "id",
                "get_applicant_link",
                "transaction_id",
                "out_trade_no",
                "handle_by",
                "created_at",
            ]
            if request.user.is_superuser
            else []
        )

    @admin.display(description="申请人", ordering="applicant__name")
    def get_applicant_name(self, obj):
        if hasattr(obj, "applicant"):
            return obj.applicant.name
        return "-"

    @admin.display(description="学校", ordering="applicant__school")
    def get_applicant_school(self, obj):
        if hasattr(obj, "applicant"):
            return obj.applicant.school
        return "-"

    @admin.display(description="微信号", ordering="applicant__wxid")
    def get_applicant_wxid(self, obj):
        if hasattr(obj, "applicant"):
            return obj.applicant.wxid
        return "-"

    @admin.display(description="申请人链接")
    def get_applicant_link(self, obj):
        if hasattr(obj, "applicant"):
            return format_html(
                '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/applicant/{}/change/">{} - {}</a>',
                obj.applicant.id,
                obj.applicant.name,
                obj.applicant.school,
            )
        return "-"

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Q
from unfold.admin import ModelAdmin

from ..models import Applicant, Match


class ApplicantHasPaidFilter(admin.SimpleListFilter):
    title = "已缴付押金"
    parameter_name = "has_paid"

    def lookups(self, request, model_admin):
        return [
            ("True", "已缴付"),
            ("False", "未缴付"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(payment__isnull=False)
        if self.value() == "False":
            return queryset.filter(payment__isnull=True)
        return queryset


class ApplicantLinkedUniFilter(admin.SimpleListFilter):
    title = "Triple Uni绑定状态"
    parameter_name = "linked_uni"

    def lookups(self, request, model_admin):
        return [
            ("linked", "已绑定"),
            ("not_linked", "未绑定"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "linked":
            return queryset.filter(linked_uni=True)
        if self.value() == "not_linked":
            return queryset.filter(linked_uni=False)
        return queryset


class ApplicantConfirmedFilter(admin.SimpleListFilter):
    title = "确认分组状态"
    parameter_name = "confirmed"

    def lookups(self, request, model_admin):
        return [
            ("confirmed", "已确认"),
            ("not_confirmed", "未确认"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "confirmed":
            return queryset.filter(confirmed=True)
        if self.value() == "not_confirmed":
            return queryset.filter(confirmed=False)
        return queryset


@admin.register(Applicant)
class ApplicantAdmin(ModelAdmin):
    search_fields = ["name", "wxid", "wechat_info__nickname", "email"]

    common_readonly_fields = [
        "id",
        "name",
        "sex",
        "grade",
        "school",
        "major",
        "email",
        "wxid",
        "wechat_info",
        "preferred_wxid",
        "continue_match",
        "comment",
        "payment",
        "updated_at",
        "created_at",
        "confirmed",
        "quitted",
    ]

    list_display = [
        "name",
        "school",
        "major",
        "grade",
        "sex",
        "get_nickname",
        "get_location",
        "get_timezone",
        "has_paid",
        "linked_uni",
        "confirmed",
        "comment",
        "quitted",
        "exclude",
        "created_at",
    ]
    list_editable = ["exclude"]
    list_filter = [
        "quitted",
        "exclude",
        ApplicantHasPaidFilter,
        ApplicantLinkedUniFilter,
        ApplicantConfirmedFilter,
        "school",
        "grade",
        "sex",
        "location",
        "timezone",
        "continue_match",
        "same_location_only",
        "preferred_sex",
        "reply_frequency",
        "created_at",
    ]
    list_display_links = [
        "name",
        "school",
        "grade",
        "sex",
        "get_nickname",
        "created_at",
    ]
    autocomplete_fields = ["wechat_info", "payment"]
    fieldsets = (
        (
            "参与的CP组",
            {"fields": ("get_matches_list",)},
        ),
        (
            "基本信息",
            {
                "fields": (
                    "id",
                    ("name", "sex", "grade", "school", "major"),
                    ("email", "wxid"),
                    "wechat_info",
                    ("timezone", "location"),
                )
            },
        ),
        (
            "MBTI信息",
            {"fields": (("mbti_ei", "mbti_sn", "mbti_tf", "mbti_jp"),)},
        ),
        (
            "个人信息",
            {
                "fields": (
                    "hobbies",
                    "fav_movies",
                    "wish",
                    "weekend_arrangement",
                    "reply_frequency",
                    "expectation",
                    "message_to_partner",
                )
            },
        ),
        (
            "匹配偏好",
            {
                "fields": (
                    ("preferred_sex", "preferred_grades", "preferred_schools"),
                    ("max_time_difference", "same_location_only"),
                    (
                        "preferred_mbti_ei",
                        "preferred_mbti_sn",
                        "preferred_mbti_tf",
                        "preferred_mbti_jp",
                    ),
                    ("preferred_wxid", "continue_match"),
                )
            },
        ),
        (
            "状态信息",
            {
                "fields": (
                    ("payment", "linked_uni"),
                    ("confirmed", "quitted", "exclude"),
                    "comment",
                )
            },
        ),
        (
            "时间戳",
            {"fields": (("created_at", "updated_at"),)},
        ),
    )
    readonly_fields = ["id", "created_at", "updated_at", "get_matches_list"]

    @admin.display(description="微信昵称", ordering="wechat_info__nickname")
    def get_nickname(self, obj):
        return obj.wechat_info.nickname

    @admin.display(description="所在地区", ordering="location")
    def get_location(self, obj):
        return Applicant.LOCATION.get(obj.location, obj.location)

    @admin.display(description="时区", ordering="timezone")
    def get_timezone(self, obj):
        return obj.timezone

    @admin.display(description="参与的CP组")
    def get_matches_list(self, obj):
        # Get all matches where this applicant is either applicant1 or applicant2
        from django.db.models import Q

        matches = (
            Match.objects.filter(Q(applicant1=obj) | Q(applicant2=obj))
            .select_related("mentor")
            .order_by("-id")[:20]
        )

        if not matches:
            return "未参与任何CP组"

        html_parts = ['<ul style="list-style: none; padding: 0;">']
        for match in matches:
            status = (
                "✓"
                if match.applicant1_status == "A" and match.applicant2_status == "A"
                else "⏳"
            )
            discarded = " (已废弃)" if match.discarded else ""
            html_parts.append(
                f'<li style="margin: 5px 0;">{status} <a class="text-primary-600 dark:text-primary-500" href="/admin/main/match/{match.id}/change/">#{match.id} - {match.name}</a>{discarded}</li>'
            )

        total_count = Match.objects.filter(
            Q(applicant1=obj) | Q(applicant2=obj)
        ).count()
        if total_count > 20:
            html_parts.append(
                f'<li style="margin: 5px 0; color: #666;">... 及其他 {total_count - 20} 组</li>'
            )
        html_parts.append("</ul>")
        return format_html("".join(html_parts))

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("wechat_info", "payment")

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return self.common_readonly_fields

    def get_exclude(self, request, obj):
        return (
            []
            if request.user.is_superuser
            else [
                "mbti_ei",
                "mbti_sn",
                "mbti_tf",
                "mbti_jp",
                "hobbies",
                "fav_movies",
                "wish",
                "weekend_arrangement",
                "reply_frequency",
                "expectation",
                "preferred_sex",
                "preferred_grades",
                "preferred_schools",
                "preferred_mbti_ei",
                "preferred_mbti_sn",
                "preferred_mbti_tf",
                "preferred_mbti_jp",
            ]
        )

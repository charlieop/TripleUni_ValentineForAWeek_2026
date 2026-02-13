from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from ..models import ExitQuestionnaire


class FutureRelationshipFilter(admin.SimpleListFilter):
    title = "活动后关系"
    parameter_name = "future_relationship"

    def lookups(self, request, model_admin):
        return list(ExitQuestionnaire.FUTURE_RELATIONSHIP_CHOICES.items())

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(future_relationship=int(self.value()))
        return queryset


@admin.register(ExitQuestionnaire)
class ExitQuestionnaireAdmin(ModelAdmin):
    list_display = [
        "get_applicant_name",
        "get_matching_satisfaction_display",
        "get_task_pace_display",
        "get_future_relationship_display",
        "get_knew_before_display",
        "recommendation_likelihood",
        "mentor_rating",
        "accept_callback",
        "created_at",
    ]
    list_display_links = [
        "get_applicant_name",
        "get_matching_satisfaction_display",
        "get_task_pace_display",
    ]
    list_filter = [
        "accept_callback",
        "matching_satisfaction",
        "task_pace",
        "knew_before",
        FutureRelationshipFilter,
        "discovery_channel",
        "participated_last_year",
    ]
    search_fields = [
        "applicant__name",
        "applicant__wxid",
        "applicant__wechat_info__nickname",
    ]
    readonly_fields = [
        "id",
        "created_at",
        "updated_at",
        "get_applicant_link",
    ]
    autocomplete_fields = ["applicant"]
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "基本信息",
            {
                "fields": (
                    "id",
                    ("applicant", "get_applicant_link"),
                ),
            },
        ),
        (
            "关于匹配算法",
            {
                "fields": (
                    "matching_satisfaction",
                    "matching_unsatisfied_reason",
                    "matching_suggestion",
                ),
            },
        ),
        (
            "关于活动任务",
            {
                "fields": (
                    "task_pace",
                    "favorite_task",
                    "least_favorite_task",
                    "task_suggestion",
                    "day7_letter_rating",
                ),
            },
        ),
        (
            "关于你们",
            {
                "fields": (
                    "heartbeat_moment",
                    "knew_before",
                    ("interaction_frequency", "interaction_frequency_other"),
                    ("future_relationship", "future_relationship_other"),
                    ("partner_engagement", "self_engagement"),
                    "partner_comment",
                ),
            },
        ),
        (
            "跨越时空的书信",
            {
                "fields": ("message_to_partner",),
            },
        ),
        (
            "Callback",
            {
                "fields": ("lamp_callback",),
                "classes": ("collapse",),
            },
        ),
        (
            "其他信息",
            {
                "fields": (
                    "participated_last_year",
                    "comparison_rating",
                    "comparison_comment",
                    ("discovery_channel", "discovery_channel_other"),
                    "recommendation_likelihood",
                    "mentor_rating",
                    "accept_callback",
                    "message_to_organizer",
                ),
            },
        ),
        (
            "时间戳",
            {
                "fields": (("created_at", "updated_at"),),
            },
        ),
    )

    # ---- custom list columns ----

    @admin.display(description="申请人", ordering="applicant__name")
    def get_applicant_name(self, obj):
        return obj.applicant.name

    @admin.display(description="匹配满意度", ordering="matching_satisfaction")
    def get_matching_satisfaction_display(self, obj):
        stars = "★" * obj.matching_satisfaction + "☆" * (5 - obj.matching_satisfaction)
        return f"{stars}"

    @admin.display(description="任务节奏", ordering="task_pace")
    def get_task_pace_display(self, obj):
        return ExitQuestionnaire.TASK_PACE_CHOICES.get(obj.task_pace, obj.task_pace)

    @admin.display(description="活动后关系", ordering="future_relationship")
    def get_future_relationship_display(self, obj):
        label = ExitQuestionnaire.FUTURE_RELATIONSHIP_CHOICES.get(
            obj.future_relationship, "未知"
        )
        if obj.future_relationship == 0:
            return format_html('<span style="color:var(--error-500,#e74c3c);font-weight:600">{}</span>', label)
        return label

    @admin.display(description="活动前是否认识", ordering="knew_before")
    def get_knew_before_display(self, obj):
        return ExitQuestionnaire.KNEW_BEFORE_CHOICES.get(obj.knew_before, obj.knew_before)

    # ---- detail page helpers ----

    @admin.display(description="申请人详情")
    def get_applicant_link(self, obj):
        if obj.applicant_id:
            url = f"/admin/main/applicant/{obj.applicant_id}/change/"
            return format_html(
                '<a class="text-primary-600 dark:text-primary-500" href="{}">{} ({})</a>',
                url,
                obj.applicant.name,
                obj.applicant.school,
            )
        return "-"

    # ---- queryset optimisation ----

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("applicant", "applicant__wechat_info")
        )

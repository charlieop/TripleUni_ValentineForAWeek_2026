from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from unfold.admin import ModelAdmin

from ..models import Match


class MatchSuccessFilter(admin.SimpleListFilter):
    title = "已成功匹配"
    parameter_name = "has_matched"

    def lookups(self, request, model_admin):
        return [
            ("True", "已成功"),
            ("False", "未成功"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(applicant1_status="A", applicant2_status="A")
        if self.value() == "False":
            return queryset.exclude(applicant1_status="A", applicant2_status="A")
        return queryset


class MatchRoundFilter(admin.SimpleListFilter):
    title = "轮次"
    parameter_name = "round"

    def lookups(self, request, model_admin):
        return [
            ("1", "第一轮"),
            ("2", "第二轮"),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(round=int(self.value()))
        return queryset


@admin.register(Match)
class MatchAdmin(ModelAdmin):
    list_display = [
        "id",
        "name",
        "get_applicant1_name",
        "get_applicant2_name",
        "get_confirmed",
        "get_round",
        "discarded",
        "get_mentor_name",
        "get_total_score",
    ]
    ordering = ["discarded", "id"]
    list_display_links = list_display
    search_fields = [
        "id",
        "name",
        "applicant1__name",
        "applicant2__name",
        "applicant1__wxid",
        "applicant2__wxid",
    ]
    readonly_fields = [
        "id",
        "get_applicant1_wxid",
        "get_applicant2_wxid",
        "get_total_score",
        "get_tasks_display",
        "created_at",
        "updated_at",
    ]
    fieldsets = (
        (
            "配对信息",
            {"fields": ("id", "name", ("mentor", "round"), "get_tasks_display")},
        ),
        (
            "嘉宾1号信息",
            {
                "fields": (
                    ("applicant1", "get_applicant1_wxid"),
                    ("applicant1_status",),
                )
            },
        ),
        (
            "嘉宾2号信息",
            {
                "fields": (
                    ("applicant2", "get_applicant2_wxid"),
                    ("applicant2_status",),
                )
            },
        ),
        (
            "状态",
            {"fields": ("discarded", "discard_reason", "get_total_score", "completed_offline_task")},
        ),
        (
            "时间戳",
            {"fields": (("created_at", "updated_at"),)},
        ),
    )
    autocomplete_fields = ["applicant1", "applicant2", "mentor"]
    date_hierarchy = "created_at"

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return self.readonly_fields + [
            "name",
            "round",
            "mentor",
            "applicant1",
            "applicant2",
            "completed_offline_task",
        ]

    def get_list_filter(self, request):
        return (
            [
                MatchSuccessFilter,
                "discarded",
                MatchRoundFilter,
                "mentor__name",
            ]
            if request.user.is_superuser
            else [MatchSuccessFilter, "discarded", MatchRoundFilter]
        )

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        self._request = request
        return super().changeform_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(mentor=request.user).filter(discarded=False)
        qs = qs.select_related(
            "applicant1",
            "applicant2",
            "mentor",
        ).prefetch_related("tasks")
        return qs

    @admin.display(description="任务列表")
    def get_tasks_display(self, obj):
        if obj is None:
            return ""
        request = getattr(self, "_request", None)
        if request and not request.user.is_superuser:
            tasks = [t for t in obj.tasks.all() if t.visible_to_mentor]
        else:
            tasks = list(obj.tasks.all())
        if not tasks:
            return format_html("<p>暂无任务</p>")
        sorted_tasks = sorted(tasks, key=lambda t: t.day)
        items = format_html_join(
            "",
            "<li style='margin: 5px 0;'><a href='{}' class='text-primary-600 dark:text-primary-500' target='_blank'>第{}天</a></li>",
            ((reverse("admin:main_task_change", args=[t.pk]), t.day) for t in sorted_tasks),
        )
        return format_html("<ul style='margin:0;padding-left:1.2em'>{}</ul>", items)

    @admin.display(description="嘉宾1", ordering="applicant1__name")
    def get_applicant1_name(self, obj):
        return f"{obj.applicant1.name} ({obj.applicant1.school})"

    @admin.display(description="嘉宾2", ordering="applicant2__name")
    def get_applicant2_name(self, obj):
        return f"{obj.applicant2.name} ({obj.applicant2.school})"

    @admin.display(description="轮次", ordering="round")
    def get_round(self, obj):
        return Match.ROUNDS.get(obj.round, obj.round)

    @admin.display(description="嘉宾1微信ID", ordering="applicant1__wxid")
    def get_applicant1_wxid(self, obj):
        return obj.applicant1.wxid

    @admin.display(description="嘉宾2微信ID", ordering="applicant2__wxid")
    def get_applicant2_wxid(self, obj):
        return obj.applicant2.wxid

    @admin.display(description="匹配成功", boolean=True)
    def get_confirmed(self, obj):
        return obj.applicant1_status == "A" and obj.applicant2_status == "A"

    @admin.display(description="Mentor", ordering="mentor__name")
    def get_mentor_name(self, obj):
        return obj.mentor.name

    @admin.display(description="总分")
    def get_total_score(self, obj):
        return obj.total_score

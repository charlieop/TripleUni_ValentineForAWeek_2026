from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import Mission


class MissionTypeFilter(admin.SimpleListFilter):
    title = "任务类型"
    parameter_name = "mission_type"

    def lookups(self, request, model_admin):
        return [
            ("daily", "每日任务 (1-7)"),
            ("secret", "秘密任务 (91-94)"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "daily":
            return queryset.filter(day__lte=7)
        if self.value() == "secret":
            return queryset.filter(day__gte=91)
        return queryset


@admin.register(Mission)
class MissionAdmin(ModelAdmin):
    list_display = [
        "get_day_display",
        "title",
        "has_content",
        "has_link",
        "updated_at",
    ]
    list_filter = [MissionTypeFilter]
    search_fields = ["title", "content"]
    readonly_fields = ["id", "created_at", "updated_at"]
    fieldsets = (
        (
            "任务信息",
            {
                "fields": (
                    "id",
                    "day",
                    "title",
                    "content",
                    "link",
                )
            },
        ),
        (
            "时间戳",
            {"fields": (("created_at", "updated_at"),)},
        ),
    )
    ordering = ["day"]

    @admin.display(description="任务类型", ordering="day")
    def get_day_display(self, obj):
        return Mission.DAY.get(obj.day, f"未知任务({obj.day})")

    @admin.display(description="有内容", boolean=True)
    def has_content(self, obj):
        return bool(obj.content)

    @admin.display(description="有链接", boolean=True)
    def has_link(self, obj):
        return bool(obj.link)

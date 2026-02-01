from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from ..models import Image


class ImageDeletedFilter(admin.SimpleListFilter):
    title = "删除状态"
    parameter_name = "deleted"

    def lookups(self, request, model_admin):
        return [
            ("active", "未删除"),
            ("deleted", "已删除"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "active":
            return queryset.filter(deleted=False)
        if self.value() == "deleted":
            return queryset.filter(deleted=True)
        return queryset


@admin.register(Image)
class ImageAdmin(ModelAdmin):
    list_display = [
        "get_thumbnail",
        "get_match_info",
        "get_day"
    ]
    list_link = [
        "get_thumbnail",
        "get_match_info",
        "get_day"
    ]
    list_filter = [
        ImageDeletedFilter,
        "task__day",
    ]
    search_fields = [
        "task__match__id",
        "task__match__name",
        "task__match__applicant1__name",
        "task__match__applicant2__name",
    ]
    autocomplete_fields = ["task"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]


    def get_list_display(self, request):
        if request.user.is_superuser:
            return self.list_display + ["deleted", "created_at"]
        return self.list_display

    def get_readonly_fields(self, request, obj=None):
        # When creating a new image, allow task selection
        # When editing, make it readonly
        if obj:  # Editing existing image
            return [
                "id",
                "task",
                "get_task_link",
                "get_match_link",
                "image_preview",
                "created_at",
            ]
        else:  # Creating new image
            return [
                "id",
                "created_at",
                "image_preview",
            ]

    def get_fieldsets(self, request, obj=None):
        if obj:  # Editing existing image
            if request.user.is_superuser:
                return (
                    (
                        "图片信息",
                        {
                            "fields": (
                                "id",
                                "get_task_link",
                                "get_match_link",
                                "image_preview",
                                "deleted",
                            )
                        },
                    ),
                    (
                        "时间戳",
                        {"fields": ("created_at",)},
                    ),
                )
            else:
                return (
                    (
                        "图片信息",
                        {
                            "fields": (
                                "get_task_link",
                                "get_match_link",
                                "image_preview",
                            )
                        },
                    ),
                )
        else:  # Creating new image
            return (
                (
                    "图片信息",
                    {
                        "fields": (
                            "task",
                            "image",
                            "deleted",
                        )
                    },
                ),
            )

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request).select_related("task", "task__match")
        return super().get_queryset(request).select_related("task", "task__match").filter(deleted=False).filter(task__match__mentor=request.user)

    @admin.display(description="缩略图")
    def get_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url,
            )
        return "无图片"

    @admin.display(description="图片预览")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 500px; max-height: 500px; border: 1px solid #ddd; border-radius: 4px; padding: 5px;" />',
                obj.image.url,
            )
        return "无图片"

    @admin.display(description="CP组", ordering="task__match__id")
    def get_match_info(self, obj):
        return f"#{obj.task.match.id} - {obj.task.match.name}"

    @admin.display(description="任务天数", ordering="task__day")
    def get_day(self, obj):
        return f"第{obj.task.day}天"

    @admin.display(description="所属任务")
    def get_task_link(self, obj):
        return format_html(
            '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/task/{}/change/">第{}天 - #{} - {}</a>',
            obj.task.id,
            obj.task.day,
            obj.task.match.id,
            obj.task.match.name,
        )

    @admin.display(description="所属CP组")
    def get_match_link(self, obj):
        return format_html(
            '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/match/{}/change/">#{} - {}</a>',
            obj.task.match.id,
            obj.task.match.id,
            obj.task.match.name,
        )

from django import forms
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.db.models import Q
from django.core.files.base import ContentFile
from unfold.admin import ModelAdmin
from PIL import Image as PILImage
from io import BytesIO
from itertools import groupby

from ..models import Task, Image, Mentor
from ..tasks import grade_batch_for_task_ids


def compress_image(image_file, max_size=(1920, 1920), quality=70):
    """
    Compress an image file while maintaining aspect ratio and quality.

    Args:
        image_file: The uploaded file
        max_size: Maximum dimensions (width, height)
        quality: JPEG quality (1-100)

    Returns:
        ContentFile with compressed image
    """
    try:
        # Open the image
        img = PILImage.open(image_file)

        # Convert RGBA to RGB if necessary (for PNG with transparency)
        if img.mode in ("RGBA", "LA", "P"):
            background = PILImage.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(
                img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None
            )
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # Resize if image is larger than max_size
        img.thumbnail(max_size, PILImage.Resampling.LANCZOS)

        # Save to BytesIO
        output = BytesIO()
        img.save(output, format="JPEG", quality=quality, optimize=True)
        output.seek(0)

        # Get original filename and change extension to .jpg
        original_name = image_file.name
        name_without_ext = original_name.rsplit(".", 1)[0]
        new_name = f"{name_without_ext}.jpg"

        return ContentFile(output.read(), name=new_name)
    except Exception as e:
        # If compression fails, return original file
        print(f"Image compression failed: {e}")
        return image_file


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class TaskCompletedFilter(admin.SimpleListFilter):
    title = "任务完成状态"
    parameter_name = "completed"

    def lookups(self, request, model_admin):
        return [
            ("completed", "已完成"),
            ("incomplete", "未完成"),
            ("has_content", "已提交内容"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "completed":
            return queryset.filter(basic_completed=True)
        if self.value() == "incomplete":
            return queryset.filter(basic_completed=False)
        if self.value() == "has_content":
            return queryset.exclude(Q(submit_text__isnull=True) | Q(submit_text=""))
        return queryset


class TaskAdminForm(forms.ModelForm):
    new_images = MultipleFileField(
        label="上传多张图片",
        required=False,
        help_text="可以一次选择多张图片上传（支持 JPG, PNG, HEIC, HEIF, WebP，每张最大5MB）。图片将自动压缩优化。",
    )

    class Meta:
        model = Task
        fields = "__all__"


def grade_batch_action(modeladmin, request, queryset):
    """Enqueue autograder grade_batch for selected tasks via Celery. Admin/superuser only."""
    if not request.user.is_superuser:
        messages.error(request, "仅管理员可执行此操作。")
        return
    tasks = list(queryset.order_by("day"))
    if not tasks:
        messages.warning(request, "请先选择要批改的任务。")
        return
    try:
        total = 0
        for day, day_tasks in groupby(tasks, key=lambda t: t.day):
            task_list = list(day_tasks)
            task_ids = [t.pk for t in task_list]
            grade_batch_for_task_ids.delay(day, task_ids)
            total += len(task_list)
        messages.success(
            request,
            f"已加入 Celery 队列，共 {total} 个任务将异步批改，请稍后在 Celery 中查看执行结果。",
        )
    except Exception as e:
        messages.error(request, f"加入队列失败: {str(e)}")


grade_batch_action.short_description = "批改选中任务 (Celery 异步，仅管理员)"


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    form = TaskAdminForm
    actions = [grade_batch_action]
    list_display = [
        "get_match_info",
        "day",
        "basic_completed",
        "basic_score",
        "bonus_score",
        "daily_score",
        "uni_score",
        "scored",
        "get_total_score",
        "get_image_count",
        "get_updated_by",
        "review",
        "completed_offline_task",
        "updated_at",
    ]
    list_filter = [
        TaskCompletedFilter,
        "basic_completed",
        "scored",
        "day",
        "match__discarded",
        "match__mentor",
        "visible_to_mentor",
        "completed_offline_task",
    ]
    search_fields = [
        "match__id",
        "match__name",
        "match__applicant1__name",
        "match__applicant2__name",
        "submit_text",
    ]
    autocomplete_fields = ["match", "updated_by"]
    date_hierarchy = "created_at"
    ordering = ["-updated_at"]

    def get_readonly_fields(self, request, obj=None):
        # When creating a new task, allow match selection
        # When editing, make it readonly
        if obj:  # Editing existing task
            if request.user.is_superuser:
                return [
                    "id",
                    "match",
                    "created_at",
                    "updated_at",
                    "get_match_link",
                    "get_images_display",
                    "get_total_score",
                ]
            else:
                return [
                    "match",
                    "day",
                    "updated_by",
                    "submit_text",
                    "get_match_link",
                    "get_images_display",
                    "get_total_score",
                ]
        else:  # Creating new task
            return [
                "id",
                "created_at",
                "updated_at",
                "get_images_display",
                "get_total_score",
            ]

    def get_fieldsets(self, request, obj=None):
        if obj:  # Editing existing task
            if not request.user.is_superuser:
                return (
                    (
                        "任务信息",
                        {
                            "fields": (
                                ("get_match_link", "day"),
                                "updated_by",
                                "submit_text",
                            )
                        },
                    ),
                    (
                        "已提交图片",
                        {"fields": ("get_images_display",), "classes": ["wide"]},
                    ),
                    (
                        "评分",
                        {
                            "fields": (
                                ("basic_completed", "completed_offline_task"),
                                (
                                    "basic_score",
                                    "bonus_score",
                                    "daily_score",
                                    "uni_score",
                                ),
                                "scored",
                                "review",
                                ("basic_review", "bonus_review"),
                                ("daily_review", "uni_review"),
                                "thinking_process",
                                "get_total_score",
                            )
                        },
                    ),
                    (
                        "上传新图片",
                        {
                            "fields": ("new_images",),
                            "description": "一次选择多张图片进行上传",
                        },
                    ),
                )
            return (
                (
                    "任务信息",
                    {
                        "fields": (
                            "id",
                            ("get_match_link", "day"),
                            "updated_by",
                            "submit_text",
                        )
                    },
                ),
                (
                    "已提交图片",
                    {"fields": ("get_images_display",), "classes": ["wide"]},
                ),
                (
                    "评分",
                    {
                        "fields": (
                            ("basic_completed", "completed_offline_task"),
                            ("basic_score", "bonus_score", "daily_score", "uni_score"),
                            "scored",
                            "review",
                            ("basic_review", "bonus_review"),
                            ("daily_review", "uni_review"),
                            "thinking_process",
                            "get_total_score",
                        )
                    },
                ),
                (
                    "上传新图片",
                    {
                        "fields": ("new_images",),
                        "description": "一次选择多张图片进行上传",
                    },
                ),
                (
                    "Mentor可见",
                    {
                        "fields": ("visible_to_mentor",),
                    },
                ),
                (
                    "时间戳",
                    {"fields": (("created_at", "updated_at"),)},
                ),
            )
        else:  # Creating new task
            return (
                (
                    "任务信息",
                    {
                        "fields": (
                            ("match", "day"),
                            "updated_by",
                            "submit_text",
                        )
                    },
                ),
                (
                    "评分",
                    {
                        "fields": (
                            ("basic_completed", "completed_offline_task"),
                            ("basic_score", "bonus_score", "daily_score", "uni_score"),
                            "scored",
                            "review",
                            ("basic_review", "bonus_review"),
                            ("daily_review", "uni_review"),
                            "thinking_process",
                        )
                    },
                ),
                (
                    "上传图片",
                    {
                        "fields": ("new_images",),
                        "description": "一次选择多张图片进行上传",
                    },
                ),
            )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser and "grade_batch_action" in actions:
            del actions["grade_batch_action"]
        return actions

    def get_list_display(self, request):
        base = list(super().get_list_display(request))
        if request.user.is_superuser:
            # Insert "last modified by" before "review"
            idx = base.index("review") if "review" in base else len(base)
            base.insert(idx, "get_last_modified_by")
        return base

    def get_queryset(self, request):
        qs = (
            super()
            .get_queryset(request)
            .select_related(
                "match", "match__applicant1", "match__applicant2", "updated_by"
            )
            .prefetch_related("imgs")
        )

        # Normal mentors should only see tasks that:
        # - belong to matches they are responsible for
        # - are explicitly marked as visible_to_mentor
        if not request.user.is_superuser:
            return qs.filter(match__mentor=request.user, visible_to_mentor=True)

        return qs

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Handle multiple file uploads with compression
        files = form.cleaned_data.get("new_images")
        if files:
            if not isinstance(files, list):
                files = [files]
            for file in files:
                if file:  # Check if file is not None
                    # Compress the image before saving
                    compressed_file = compress_image(file)
                    Image.objects.create(task=obj, image=compressed_file)

    @admin.display(description="CP组", ordering="match__id")
    def get_match_info(self, obj):
        return f"#{obj.match.id} - {obj.match.name}"

    @admin.display(description="CP组链接")
    def get_match_link(self, obj):
        return format_html(
            '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/match/{}/change/">#{} - {}</a>',
            obj.match.id,
            obj.match.id,
            obj.match.name,
        )

    @admin.display(description="总分")
    def get_total_score(self, obj):
        return obj.basic_score + obj.bonus_score + obj.daily_score + obj.uni_score

    @admin.display(description="图片数量")
    def get_image_count(self, obj):
        return obj.imgs.filter(deleted=False).count()

    @admin.display(description="最后修改者")
    def get_last_modified_by(self, obj):
        """Only shown in list_display for superusers. Shows username of last admin change from LogEntry."""
        if obj.pk is None:
            return "-"
        ct = ContentType.objects.get_for_model(Task)
        entry = (
            LogEntry.objects.filter(
                content_type=ct, object_id=str(obj.pk)
            )
            .order_by("-action_time")
            .select_related("user")
            .first()
        )
        if entry and entry.user:
            return f"{entry.user.get_username()}"
        return "-"

    @admin.display(description="最后提交者", ordering="updated_by__name")
    def get_updated_by(self, obj):
        if obj.updated_by:
            return obj.updated_by.name
        return "-"

    @admin.display(description="提交的图片")
    def get_images_display(self, obj):
        images = obj.imgs.filter(deleted=False)
        if not images:
            return "无图片"

        container_style = """
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            overflow-y: auto;
            height: 85vh;
            width: 100%;
            margin: 0;
            gap: 15px;
            padding: 10px;
            # background: #f5f5f5;
            border-radius: 8px;
        """

        image_style = """
            height: calc(85vh - 20px);
            background: none;
            border-radius: 8px;
            width: auto;
            max-width: 100%;
            object-fit: contain;
            flex-shrink: 0;
        """

        html_parts = [f'<div style="{container_style}">']
        for img in images:
            html_parts.append(f'<img src="{img.image.url}" style="{image_style}"/>')
        html_parts.append("</div>")

        return format_html("".join(html_parts))

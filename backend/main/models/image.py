import uuid
from django.db import models
from django.core.exceptions import ValidationError

SIZE_LIMIT = 5 * 1024 * 1024

VALID_MIME_TYPES = [
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/heic",
    "image/heif",
    "image/webp",
]

VALID_FILE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".heic",
    ".heif",
    ".webp",
]

def check_image(value) -> None:
    """Validator for image field - checks size and MIME type"""
    if value.size > SIZE_LIMIT:
        raise ValidationError({"detail": "File too large. Size should not exceed 5MB."})

    # Try to get content type from the file
    if hasattr(value, "content_type"):
        file_mime_type = value.content_type
    elif hasattr(value, "file") and hasattr(value.file, "content_type"):
        file_mime_type = value.file.content_type
    else:
        # Fallback: check file extension
        file_name = value.name.lower() if hasattr(value, "name") else ""
        if any(
            file_name.endswith(ext)
            for ext in VALID_FILE_EXTENSIONS
        ):
            return
        raise ValidationError(
            {"detail": "Unsupported file type. Only JPEG, PNG, JPG, HEIC, HEIF and WebP are allowed."}
        )

    if file_mime_type not in VALID_MIME_TYPES:
        raise ValidationError(
            {"detail": "Unsupported file type. Only JPEG, PNG, JPG, HEIC, HEIF and WebP are allowed."}
        )


class Image(models.Model):
    def generateUploadPath(self, filename: str) -> str:
        ext = filename.split(".")[-1]
        modified_filename = "{}.{}".format(self.id, ext)
        return f"uploads/tasks/{self.task.match.id}/day-{self.task.day}/{modified_filename}"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    task = models.ForeignKey(
        "Task", on_delete=models.CASCADE, related_name="imgs", verbose_name="对应任务"
    )
    image = models.ImageField(
        upload_to=generateUploadPath, validators=[check_image], verbose_name="图片"
    )

    deleted = models.BooleanField(default=False, verbose_name="已删除")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"#{self.task.match.id}-{self.task.match.name}  第{self.task.day}天 - {self.image.url}"

    class Meta:
        verbose_name = "任务图片"
        verbose_name_plural = "任务图片"
        db_table = "image"
        ordering = ["task", "created_at"]

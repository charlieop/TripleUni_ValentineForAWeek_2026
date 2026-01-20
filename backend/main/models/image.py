import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.forms.fields import ImageField


class Image(models.Model):
    def generateUploadPath(self, filename: str) -> str:
        ext = filename.split(".")[-1]
        modified_filename = "{}.{}".format(self.id, ext)
        return f"uploads/tasks/{self.task.match.id}/day-{self.task.day}/{modified_filename}"

    def check_image(value: ImageField) -> None:
        SIZE_LIMIT = 5 * 1024 * 1024
        if value.size > SIZE_LIMIT:
            raise ValidationError("File too large. Size should not exceed 5 MiB.")
        valid_mime_types = ["image/jpeg", "image/png", "image/jpg", "image/heic"]
        file_mime_type = value.file.content_type
        if file_mime_type not in valid_mime_types:
            raise ValidationError(
                "Unsupported file type. Only JPEG, PNG, JPG and HEIC are allowed."
            )

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

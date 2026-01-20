import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class Mentor(AbstractUser):
    def generateUploadPath(self, filename: str) -> str:
        ext = filename.split(".")[-1]
        modified_filename = "{}.{}".format(self.id, ext)
        return f"uploads/mentor-qr-code/{modified_filename}"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=10, verbose_name="姓名")
    wechat = models.CharField(max_length=30, verbose_name="微信号")
    wechat_qrcode = models.ImageField(
        upload_to=generateUploadPath, null=True, blank=True, verbose_name="微信二维码"
    )

    # Override groups and user_permissions to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this mentor belongs to.",
        related_name="mentor_set",
        related_query_name="mentor",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this mentor.",
        related_name="mentor_set",
        related_query_name="mentor",
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Mentor"
        verbose_name_plural = "Mentors"
        db_table = "mentor"
        ordering = ["created_at"]

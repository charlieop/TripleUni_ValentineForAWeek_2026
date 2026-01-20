from django.db import models
import uuid


class Token(models.Model):
    token = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, verbose_name="Token")
    wechat_info = models.OneToOneField(
        "WeChatInfo",
        on_delete=models.PROTECT,
        related_name="token",
        db_index=True,
        verbose_name="微信信息",
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.wechat_info.nickname} - {self.token}"

    class Meta:
        verbose_name = "登录凭证"
        verbose_name_plural = "登录凭证"
        db_table = "token"
        ordering = ["created_at"]

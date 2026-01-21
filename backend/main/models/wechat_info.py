from django.db import models
from uuid import uuid4


class WeChatInfo(models.Model):
    def generateUploadPath(self, filename: str) -> str:
        ext = filename.split(".")[-1]
        modified_filename = "{}.{}".format(uuid4(), ext)
        return f"uploads/wechat-headimg/{modified_filename}"

    openid = models.CharField(max_length=50, primary_key=True, verbose_name="OpenID")
    unionid = models.CharField(max_length=50, db_index=True, verbose_name="UnionID")

    nickname = models.CharField(max_length=50, verbose_name="昵称")
    head_image = models.ImageField(upload_to=generateUploadPath, verbose_name="头像")
    head_image_url = models.URLField(verbose_name="头像URL")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.nickname}"

    class Meta:
        verbose_name = "微信信息"
        verbose_name_plural = "微信信息"
        db_table = "wechat_info"
        ordering = ["nickname"]

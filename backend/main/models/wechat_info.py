from django.db import models
from django.core.cache import cache
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Invalidate cache for token-based queries
        try:
            token = self.token
            cache.delete(f"token:{token.token}:openid")
            cache.delete(f"token:{token.token}:wechat_info")
            cache.delete(f"token:{token.token}:applicant")
        except:
            pass
        # Invalidate applicant cache by openid
        cache.delete(f"applicant:openid:{self.openid}")

    def delete(self, *args, **kwargs):
        # Store values before deletion for cache invalidation
        openid = self.openid
        token_str = None
        try:
            token = self.token
            token_str = str(token.token)
        except:
            pass

        super().delete(*args, **kwargs)

        # Invalidate cache
        if token_str:
            cache.delete(f"token:{token_str}:openid")
            cache.delete(f"token:{token_str}:wechat_info")
            cache.delete(f"token:{token_str}:applicant")
        cache.delete(f"applicant:openid:{openid}")

    def __str__(self):
        return f"{self.nickname}"

    class Meta:
        verbose_name = "微信信息"
        verbose_name_plural = "微信信息"
        db_table = "wechat_info"
        ordering = ["nickname"]

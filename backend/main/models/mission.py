import uuid
from django.db import models
from django.core.cache import cache

class Mission(models.Model):
    DAY = { 
        1: "第一天任务",
        2: "第二天任务",
        3: "第三天任务",
        4: "第四天任务",
        5: "第五天任务",
        6: "第六天任务",
        7: "第七天任务",
        91: "秘密任务1",
        92: "秘密任务2",
        93: "秘密任务3",
        94: "秘密任务4",
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    day = models.IntegerField(choices=DAY, unique=True, verbose_name="任务类型")

    title = models.CharField(max_length=50, verbose_name="标题")
    content = models.TextField(blank=True, null=True, verbose_name="内容")
    link = models.URLField(blank=True, null=True, verbose_name="链接")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Invalidate mission cache
        cache.delete(f"mission:day:{self.day}")
        
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # Invalidate mission cache
        cache.delete(f"mission:day:{self.day}")

    def __str__(self):
        return f"{Mission.DAY[self.day]}: {self.title}"

    class Meta:
        verbose_name = "发布任务"
        verbose_name_plural = "发布任务"
        db_table = "mission"
        ordering = ["day"]

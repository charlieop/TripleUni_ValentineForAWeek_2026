import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.cache import cache


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    match = models.ForeignKey(
        "Match", on_delete=models.PROTECT, related_name="tasks", verbose_name="对应CP组"
    )
    day = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)], verbose_name="第X天"
    )

    submit_text = models.TextField(blank=True, null=True, verbose_name="提交内容")

    visible_to_mentor = models.BooleanField(
        default=False,
        verbose_name="对Mentor可见",
        help_text="仅当为 True 时，普通 Mentor 才能在后台看到该任务。",
    )

    updated_by = models.ForeignKey(
        "Applicant",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="updated_tasks",
        verbose_name="最后提交者",
    )

    basic_completed = models.BooleanField(default=False, verbose_name="主线任务完成")
    basic_score = models.IntegerField(default=0, verbose_name="主线任务分数")
    bonus_score = models.IntegerField(default=0, verbose_name="支线&Bonus任务分数")
    daily_score = models.IntegerField(default=0, verbose_name="日常任务分数")
    uni_score = models.IntegerField(default=0, verbose_name="Triple Uni分数")
    
    basic_review = models.TextField(blank=True, null=True, verbose_name="主线任务评分备注")
    bonus_review = models.TextField(blank=True, null=True, verbose_name="支线&Bonus任务评分备注")
    daily_review = models.TextField(blank=True, null=True, verbose_name="日常任务评分备注")
    uni_review = models.TextField(blank=True, null=True, verbose_name="Triple Uni评分备注")
    thinking_process = models.TextField(blank=True, null=True, verbose_name="模型思考过程")

    scored = models.BooleanField(default=False, verbose_name="已评分")
    review = models.TextField(blank=True, null=True, verbose_name="评分备注(只有 Mentor 可见)")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Store old values before save for cache invalidation
        old_match_id = None
        old_day = None
        if self.pk:
            try:
                old_instance = Task.objects.get(pk=self.pk)
                old_match_id = old_instance.match_id
                old_day = old_instance.day
            except Task.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        # Invalidate task cache for this match and day
        cache.delete(f"task:match:{self.match.id}:day:{self.day}")
        # Invalidate old task cache if match or day changed
        if old_match_id and (old_match_id != self.match_id or old_day != self.day):
            cache.delete(f"task:match:{old_match_id}:day:{old_day}")

        # Note: We don't invalidate ranking cache here to allow it to persist for full 15 minutes
        # The ranking cache will be recalculated on next get_rank() call after expiration
        if self.match:
            cache.delete(f"match:applicant:{self.match.applicant1_id}")
            cache.delete(f"match:applicant:{self.match.applicant2_id}")

    def delete(self, *args, **kwargs):
        # Store values before deletion for cache invalidation
        match_id = self.match_id if self.match else None
        day = self.day
        applicant1_id = None
        applicant2_id = None
        if self.match:
            applicant1_id = self.match.applicant1_id
            applicant2_id = self.match.applicant2_id

        super().delete(*args, **kwargs)

        # Invalidate cache
        from django.core.cache import cache

        if match_id:
            cache.delete(f"task:match:{match_id}:day:{day}")
        # Invalidate ranking cache when task is deleted
        if applicant1_id:
            cache.delete(f"match:applicant:{applicant1_id}")
        if applicant2_id:
            cache.delete(f"match:applicant:{applicant2_id}")

    def __str__(self):
        return f"第{self.day}天: #{self.match.id}-{self.match.name}"

    class Meta:
        verbose_name = "任务"
        verbose_name_plural = "任务"
        db_table = "task"
        ordering = ["day", "created_at"]
        unique_together = [["match", "day"]]

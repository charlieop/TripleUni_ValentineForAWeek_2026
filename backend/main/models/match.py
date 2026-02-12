from django.db import models
from django.core.cache import cache


class Match(models.Model):
    ROUNDS = {1: "第一轮", 2: "第二轮"}
    STATUS = {"A": "已接受", "R": "已拒绝", "P": "待确认"}

    id = models.AutoField(primary_key=True, editable=False, verbose_name="组号")
    name = models.CharField(max_length=50, default="取一个组名吧!", verbose_name="组名")

    round = models.IntegerField(choices=ROUNDS, verbose_name="轮次")

    mentor = models.ForeignKey(
        "Mentor",
        on_delete=models.PROTECT,
        related_name="matches",
        verbose_name="负责Mentor",
    )
    applicant1 = models.ForeignKey(
        "Applicant", on_delete=models.PROTECT, related_name="+", verbose_name="嘉宾1号"
    )
    applicant1_status = models.CharField(
        max_length=1, choices=STATUS, default="P", verbose_name="嘉宾1号状态"
    )

    applicant2 = models.ForeignKey(
        "Applicant", on_delete=models.PROTECT, related_name="+", verbose_name="嘉宾2号"
    )
    applicant2_status = models.CharField(
        max_length=1, choices=STATUS, default="P", verbose_name="嘉宾2号状态"
    )

    @property
    def total_score(self):
        return sum(
            task.basic_score + task.bonus_score + task.daily_score + task.uni_score
            for task in self.tasks.all()
        )

    discarded = models.BooleanField(default=False, verbose_name="已废弃")
    discard_reason = models.TextField(blank=True, null=True, verbose_name="废弃原因")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Store old values before save for cache invalidation
        old_applicant1_id = None
        old_applicant2_id = None
        if self.pk:
            try:
                old_instance = Match.objects.get(pk=self.pk)
                old_applicant1_id = old_instance.applicant1_id
                old_applicant2_id = old_instance.applicant2_id
            except Match.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        # Invalidate match cache for both applicants
        if self.applicant1:
            cache.delete(f"match:applicant:{self.applicant1.id}")
        if self.applicant2:
            cache.delete(f"match:applicant:{self.applicant2.id}")
        # Invalidate old applicants if they changed
        if old_applicant1_id and old_applicant1_id != self.applicant1_id:
            cache.delete(f"match:applicant:{old_applicant1_id}")
        if old_applicant2_id and old_applicant2_id != self.applicant2_id:
            cache.delete(f"match:applicant:{old_applicant2_id}")

        # Note: We don't invalidate ranking cache here to allow it to persist for full 15 minutes
        # The ranking cache will be recalculated on next get_rank() call after expiration

    def delete(self, *args, **kwargs):
        # Store values before deletion for cache invalidation
        applicant1_id = self.applicant1_id if self.applicant1 else None
        applicant2_id = self.applicant2_id if self.applicant2 else None

        super().delete(*args, **kwargs)

        # Invalidate cache
        from django.core.cache import cache

        if applicant1_id:
            cache.delete(f"match:applicant:{applicant1_id}")
        if applicant2_id:
            cache.delete(f"match:applicant:{applicant2_id}")
        # Invalidate ranking cache when match is deleted
        cache.delete("match:ranking:all")

    def __str__(self):
        return f"#{self.id}-{self.name}  | Mentor: {self.mentor.name}"

    class Meta:
        verbose_name = "CP组"
        verbose_name_plural = "CP组"
        db_table = "match"
        ordering = ["id"]

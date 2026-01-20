import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    match = models.ForeignKey(
        "Match", on_delete=models.PROTECT, related_name="tasks", verbose_name="对应CP组"
    )
    day = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)], verbose_name="第X天"
    )

    submit_text = models.TextField(blank=True, null=True, verbose_name="提交内容")
    submit_by = models.ForeignKey(
        "Applicant",
        on_delete=models.PROTECT,
        related_name="created_tasks",
        verbose_name="创建者",
    )

    basic_completed = models.BooleanField(default=False, verbose_name="基础任务完成")
    basic_score = models.IntegerField(default=0, verbose_name="基础任务分数")
    bonus_score = models.IntegerField(default=0, verbose_name="支线&Bonus任务分数")
    daily_score = models.IntegerField(default=0, verbose_name="日常任务分数")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"第{self.day}天: #{self.match.id}-{self.match.name}"

    class Meta:
        verbose_name = "任务"
        verbose_name_plural = "任务"
        db_table = "task"
        ordering = ["day", "created_at"]

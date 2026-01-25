from django.db import models


class Match(models.Model):
    ROUNDS = {1: "第一轮", 2: "第二轮"}
    STATUS = {"A": "已接受", "R": "已拒绝", "P": "待确认"}

    id = models.AutoField(primary_key=True, editable=False, verbose_name="组号")
    name = models.CharField(max_length=30, default="取一个组名吧!", verbose_name="组名")

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
            task.basic_score + task.bonus_score + task.daily_score
            for task in self.tasks.all()
        )

    discarded = models.BooleanField(default=False, verbose_name="已废弃")
    discard_reason = models.TextField(blank=True, null=True, verbose_name="废弃原因")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id}-{self.name}  | Mentor: {self.mentor.name}"

    class Meta:
        verbose_name = "CP组"
        verbose_name_plural = "CP组"
        db_table = "match"
        ordering = ["id"]

from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


class ExitQuestionnaire(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    applicant = models.OneToOneField(
        "Applicant",
        on_delete=models.CASCADE,
        related_name="exit_questionnaire",
        verbose_name="申请人",
    )

    # ========== 关于匹配算法 ==========
    matching_satisfaction = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="匹配满意度",
    )
    matching_unsatisfied_reason = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="匹配不满意原因"
    )
    matching_suggestion = models.TextField(
        max_length=100, blank=True, null=True, verbose_name="匹配算法建议"
    )

    # ========== 关于活动任务 ==========
    TASK_PACE_CHOICES = {
        0: "过于暧昧",
        1: "节奏刚刚好",
        2: "希望更亲近",
    }
    task_pace = models.IntegerField(
        choices=TASK_PACE_CHOICES, verbose_name="任务节奏评价"
    )
    favorite_task = models.TextField(
        max_length=100, verbose_name="最喜欢的任务"
    )
    least_favorite_task = models.TextField(
        max_length=100, verbose_name="最不喜欢的任务"
    )
    task_suggestion = models.TextField(
        max_length=100, blank=True, null=True, verbose_name="任务设置建议"
    )
    day7_letter_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Day7信件评分",
    )

    # ========== 关于你们 ==========
    heartbeat_moment = models.TextField(
        max_length=200, verbose_name="心动时刻"
    )
    KNEW_BEFORE_CHOICES = {
        0: "完全不认识",
        1: "见过/听说过但没有微信",
        2: "有微信但不熟",
        3: "朋友来参加活动",
        4: "情侣来参加活动",
    }
    knew_before = models.IntegerField(
        choices=KNEW_BEFORE_CHOICES, verbose_name="活动前是否认识"
    )
    INTERACTION_FREQUENCY_CHOICES = {
        0: "每天多次",
        1: "每天几次",
        2: "仅为完成任务",
        3: "有时一整天没说话",
        4: "其它",
    }
    interaction_frequency = models.IntegerField(
        choices=INTERACTION_FREQUENCY_CHOICES, verbose_name="互动频率"
    )
    interaction_frequency_other = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="互动频率补充"
    )
    FUTURE_RELATIONSHIP_CHOICES = {
        0: "已经在一起",
        1: "希望进一步了解",
        2: "继续做好朋友",
        3: "做普通朋友",
        4: "不会再主动联络",
        5: "已经没有再说话",
        6: "其它",
    }
    future_relationship = models.IntegerField(
        choices=FUTURE_RELATIONSHIP_CHOICES, verbose_name="活动后关系"
    )
    future_relationship_other = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="活动后关系补充"
    )
    partner_engagement = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="对方投入度",
    )
    self_engagement = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="自己投入度",
    )
    partner_comment = models.TextField(
        max_length=100, blank=True, null=True, verbose_name="关于ta的补充"
    )

    # ========== 跨越时空的书信 ==========
    message_to_partner = models.TextField(
        max_length=500, verbose_name="给ta的话"
    )

    # ========== Callback ==========
    lamp_callback = models.TextField(
        max_length=100, blank=True, null=True, verbose_name="路灯callback"
    )

    # ========== 其他信息 ==========
    participated_last_year = models.BooleanField(
        blank=True, null=True, verbose_name="去年是否参加"
    )
    comparison_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True,
        null=True,
        verbose_name="与去年对比评分",
    )
    comparison_comment = models.TextField(
        max_length=100, blank=True, null=True, verbose_name="与去年对比评价"
    )
    DISCOVERY_CHANNEL_CHOICES = {
        0: "Triple Uni小程序或公众号",
        1: "其他微信公众号",
        2: "朋友转发",
        3: "其它社交平台",
        4: "本身就知道",
        5: "其它",
    }
    discovery_channel = models.IntegerField(
        choices=DISCOVERY_CHANNEL_CHOICES, verbose_name="了解渠道"
    )
    discovery_channel_other = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="了解渠道补充"
    )
    recommendation_likelihood = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="推荐意愿",
    )
    mentor_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Mentor评分",
    )
    accept_callback = models.BooleanField(
        default=True, verbose_name="是否愿意接受回访"
    )
    message_to_organizer = models.TextField(
        max_length=200, blank=True, null=True, verbose_name="给主办方的话"
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"退出问卷-{self.applicant.name}-{'愿意' if self.accept_callback else '不愿意'}接受回访"

    class Meta:
        verbose_name = "退出问卷"
        verbose_name_plural = "退出问卷"
        db_table = "exit_questionnaire"

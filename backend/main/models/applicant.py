import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib import admin


class Applicant(models.Model):
    SCHOOL_LABELS = {"UST": "UST", "HKU": "HKU", "CUHK": "CU"}
    GRADE = {
        "UG1": "大一",
        "UG2": "大二",
        "UG3": "大三",
        "UG4": "大四",
        "UG5": "大五",
        "MS": "硕士",
        "PHD": "博士",
        "PROF": "教授",
    }
    SEX = {"M": "男", "F": "女"}
    MBTI_EI = {"e": "外向e", "i": "内向i", "x": "无"}
    MBTI_SN = {"s": "感觉s", "n": "直觉n", "x": "无"}
    MBTI_TF = {"t": "思维t", "f": "情感f", "x": "无"}
    MBTI_JP = {"j": "判断j", "p": "感知p", "x": "无"}

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=10, verbose_name="姓名")
    sex = models.CharField(max_length=1, choices=SEX, verbose_name="性别")
    grade = models.CharField(max_length=4, choices=GRADE, verbose_name="年级")
    school = models.CharField(max_length=4, choices=SCHOOL_LABELS, verbose_name="学校")
    email = models.EmailField(unique=True, verbose_name="邮箱")
    wxid = models.CharField(unique=True, max_length=50, verbose_name="微信号")
    wechat_info = models.OneToOneField(
        "WeChatInfo",
        on_delete=models.PROTECT,
        related_name="applicant",
        db_index=True,
        verbose_name="微信信息",
    )

    mbti_ei = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="MBTI-EI",
    )
    mbti_sn = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="MBTI-SN",
    )
    mbti_tf = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="MBTI-TF",
    )
    mbti_jp = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="MBTI-JP",
    )

    preferred_sex = models.CharField(max_length=1, choices=SEX, verbose_name="性别要求")
    preferred_grades = models.CharField(max_length=30, verbose_name="年级要求")
    preferred_schools = models.CharField(max_length=20, verbose_name="学校要求")

    preferred_mbti_ei = models.CharField(
        max_length=1, choices=MBTI_EI, verbose_name="MBTI-EI偏好"
    )
    preferred_mbti_sn = models.CharField(
        max_length=1, choices=MBTI_SN, verbose_name="MBTI-SN偏好"
    )
    preferred_mbti_tf = models.CharField(
        max_length=1, choices=MBTI_TF, verbose_name="MBTI-TF偏好"
    )
    preferred_mbti_jp = models.CharField(
        max_length=1, choices=MBTI_JP, verbose_name="MBTI-JP偏好"
    )

    preferred_wxid = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="匹配对象偏好"
    )
    continue_match = models.BooleanField(default=True, verbose_name="愿意继续匹配")

    message_to_partner = models.TextField(
        max_length=50, blank=True, null=True, verbose_name="给对方的留言"
    )

    comment = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="留言"
    )

    payment = models.OneToOneField(
        "PaymentRecord",
        on_delete=models.PROTECT,
        related_name="applicant",
        null=True,
        blank=True,
        verbose_name="付款凭证",
    )

    @admin.display(boolean=True, description="押金已支付")
    def has_paid(self):
        return self.payment is not None

    quitted = models.BooleanField(default=False, verbose_name="已退出")
    exclude = models.BooleanField(default=False, verbose_name="人工排除")

    confirmed = models.BooleanField(default=False, verbose_name="已确认分组")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}-{Applicant.SEX[self.sex]}-{self.school}-{Applicant.GRADE[self.grade]}"

    class Meta:
        verbose_name = "申请人"
        verbose_name_plural = "申请人"
        db_table = "applicant"
        ordering = ["created_at"]

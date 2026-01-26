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
    TIMEZONE = {
        "UTC-12": "UTC-12:00 (贝克岛)",
        "UTC-11": "UTC-11:00 (美属萨摩亚)",
        "UTC-10": "UTC-10:00 (夏威夷)",
        "UTC-9": "UTC-09:00 (阿拉斯加)",
        "UTC-8": "UTC-08:00 (太平洋时间, 洛杉矶、温哥华)",
        "UTC-7": "UTC-07:00 (山地时间, 丹佛、凤凰城)",
        "UTC-6": "UTC-06:00 (中部时间, 芝加哥、墨西哥城)",
        "UTC-5": "UTC-05:00 (东部时间, 纽约、多伦多)",
        "UTC-4": "UTC-04:00 (大西洋时间, 哈利法克斯、圣地亚哥)",
        "UTC-3": "UTC-03:00 (巴西、阿根廷)",
        "UTC-2": "UTC-02:00 (南乔治亚)",
        "UTC-1": "UTC-01:00 (亚速尔群岛)",
        "UTC+0": "UTC+00:00 (伦敦、都柏林)",
        "UTC+1": "UTC+01:00 (柏林、巴黎)",
        "UTC+2": "UTC+02:00 (开罗、雅典)",
        "UTC+3": "UTC+03:00 (莫斯科、迪拜)",
        "UTC+4": "UTC+04:00 (阿布扎比)",
        "UTC+5": "UTC+05:00 (巴基斯坦)",
        "UTC+5.5": "UTC+05:30 (印度)",
        "UTC+6": "UTC+06:00 (孟加拉国)",
        "UTC+7": "UTC+07:00 (曼谷、雅加达)",
        "UTC+8": "UTC+08:00 (北京、香港、新加坡)",
        "UTC+9": "UTC+09:00 (东京、首尔)",
        "UTC+10": "UTC+10:00 (悉尼、墨尔本)",
        "UTC+11": "UTC+11:00 (所罗门群岛)",
        "UTC+12": "UTC+12:00 (奥克兰、惠灵顿)",
    }
    LOCATION = {
        "HK": "香港",
        "SZ": "深圳",
        "GD": "广东省",
        "TW": "台湾",
        "CN": "中国",
        "JP_KR": "日韩",
        "ASIA": "亚洲",
        "OCEANIA": "大洋洲",
        "UK": "英国",
        "EU": "欧洲",
        "US": "美国",
        "CA": "加拿大",
        "NA": "北美洲",
        "OTHER": "其他",
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=10, verbose_name="姓名")
    sex = models.CharField(max_length=1, choices=SEX, verbose_name="性别")
    grade = models.CharField(max_length=4, choices=GRADE, verbose_name="年级")
    school = models.CharField(max_length=4, choices=SCHOOL_LABELS, verbose_name="学校")
    email = models.EmailField(unique=True, verbose_name="邮箱")
    wxid = models.CharField(unique=True, max_length=50, verbose_name="微信号")
    timezone = models.CharField(
        max_length=10, choices=TIMEZONE, default="UTC+8", verbose_name="时区"
    )
    location = models.CharField(
        max_length=10, choices=LOCATION, default="HK", verbose_name="所在地区"
    )
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
    max_time_difference = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(12)],
        default=3,
        verbose_name="最大时差",
    )
    same_location_only = models.BooleanField(default=False, verbose_name="仅匹配同地区")

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

    hobbies = models.CharField(
        max_length=50, null=False, blank=False, verbose_name="兴趣爱好"
    )
    fav_movies = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name="最喜欢的书/电影/动漫/电视剧",
    )
    wish = models.CharField(
        max_length=50, null=False, blank=False, verbose_name="阿拉丙神灯愿望"
    )
    weekend_arrangement = models.CharField(
        max_length=50, null=False, blank=False, verbose_name="周末安排"
    )
    REPLY_FREQUENCY_CHOICES = {
        "1": "开启勿扰模式, 闲下来再回",
        "2": "攒很多消息, 逐一回复",
        "3": "佛系查看, 不定时回复",
        "4": "经常看手机, 看到就回",
        "5": "一直在线, 基本秒回",
    }
    reply_frequency = models.CharField(
        max_length=1,
        choices=REPLY_FREQUENCY_CHOICES,
        null=False,
        blank=False,
        verbose_name="聊天习惯",
    )
    expectation = models.CharField(
        max_length=50, null=False, blank=False, verbose_name="期待的关系"
    )

    linked_uni = models.BooleanField(default=False, verbose_name="是否绑定triple uni")

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

from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    WeChatInfo,
    Token,
    Applicant,
    PaymentRecord,
    Mentor,
    Match,
    Task,
    Image,
    Mission,
)
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.html import format_html
from django.db.models import Q


class ApplicantHasPaidFilter(admin.SimpleListFilter):
    title = "已缴付押金"
    parameter_name = "has_paid"

    def lookups(self, request, model_admin):
        return [
            ("True", "已缴付"),
            ("False", "未缴付"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(payment__isnull=False)
        if self.value() == "False":
            return queryset.filter(payment__isnull=True)
        return queryset


class ApplicantLinkedUniFilter(admin.SimpleListFilter):
    title = "Triple Uni绑定状态"
    parameter_name = "linked_uni"

    def lookups(self, request, model_admin):
        return [
            ("linked", "已绑定"),
            ("not_linked", "未绑定"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "linked":
            return queryset.filter(linked_uni=True)
        if self.value() == "not_linked":
            return queryset.filter(linked_uni=False)
        return queryset


class ApplicantConfirmedFilter(admin.SimpleListFilter):
    title = "确认分组状态"
    parameter_name = "confirmed"

    def lookups(self, request, model_admin):
        return [
            ("confirmed", "已确认"),
            ("not_confirmed", "未确认"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "confirmed":
            return queryset.filter(confirmed=True)
        if self.value() == "not_confirmed":
            return queryset.filter(confirmed=False)
        return queryset


@admin.register(Applicant)
class ApplicantAdmin(ModelAdmin):
    search_fields = ["name", "wxid", "wechat_info__nickname", "email"]

    common_readonly_fields = [
        "id",
        "name",
        "sex",
        "grade",
        "school",
        "email",
        "wxid",
        "wechat_info",
        "preferred_wxid",
        "continue_match",
        "comment",
        "payment",
        "updated_at",
        "created_at",
        "confirmed",
        "quitted",
    ]

    list_display = [
        "name",
        "school",
        "grade",
        "sex",
        "get_nickname",
        "get_location",
        "get_timezone",
        "has_paid",
        "linked_uni",
        "confirmed",
        "comment",
        "quitted",
        "exclude",
        "created_at",
    ]
    list_editable = ["exclude"]
    list_filter = [
        "quitted",
        "exclude",
        ApplicantHasPaidFilter,
        ApplicantLinkedUniFilter,
        ApplicantConfirmedFilter,
        "school",
        "grade",
        "sex",
        "location",
        "timezone",
        "continue_match",
        "same_location_only",
        "preferred_sex",
        "reply_frequency",
        "created_at",
    ]
    list_display_links = [
        "name",
        "school",
        "grade",
        "sex",
        "get_nickname",
        "created_at",
    ]
    autocomplete_fields = ["wechat_info", "payment"]
    fieldsets = (
        (
            "参与的CP组",
            {"fields": ("get_matches_list",)},
        ),
        (
            "基本信息",
            {
                "fields": (
                    "id",
                    ("name", "sex", "grade", "school"),
                    ("email", "wxid"),
                    "wechat_info",
                    ("timezone", "location"),
                )
            },
        ),
        (
            "MBTI信息",
            {"fields": (("mbti_ei", "mbti_sn", "mbti_tf", "mbti_jp"),)},
        ),
        (
            "个人信息",
            {
                "fields": (
                    "hobbies",
                    "fav_movies",
                    "wish",
                    "weekend_arrangement",
                    "reply_frequency",
                    "expectation",
                    "message_to_partner",
                )
            },
        ),
        (
            "匹配偏好",
            {
                "fields": (
                    ("preferred_sex", "preferred_grades", "preferred_schools"),
                    ("max_time_difference", "same_location_only"),
                    (
                        "preferred_mbti_ei",
                        "preferred_mbti_sn",
                        "preferred_mbti_tf",
                        "preferred_mbti_jp",
                    ),
                    ("preferred_wxid", "continue_match"),
                )
            },
        ),
        (
            "状态信息",
            {
                "fields": (
                    ("payment", "linked_uni"),
                    ("confirmed", "quitted", "exclude"),
                    "comment",
                )
            },
        ),
        (
            "时间戳",
            {"fields": (("created_at", "updated_at"),)},
        ),
    )
    readonly_fields = ["id", "created_at", "updated_at", "get_matches_list"]

    @admin.display(description="微信昵称", ordering="wechat_info__nickname")
    def get_nickname(self, obj):
        return obj.wechat_info.nickname

    @admin.display(description="所在地区", ordering="location")
    def get_location(self, obj):
        return Applicant.LOCATION.get(obj.location, obj.location)

    @admin.display(description="时区", ordering="timezone")
    def get_timezone(self, obj):
        return obj.timezone

    @admin.display(description="参与的CP组")
    def get_matches_list(self, obj):
        # Get all matches where this applicant is either applicant1 or applicant2
        from django.db.models import Q

        matches = (
            Match.objects.filter(Q(applicant1=obj) | Q(applicant2=obj))
            .select_related("mentor")
            .order_by("-id")[:20]
        )

        if not matches:
            return "未参与任何CP组"

        html_parts = ['<ul style="list-style: none; padding: 0;">']
        for match in matches:
            status = (
                "✓"
                if match.applicant1_status == "A" and match.applicant2_status == "A"
                else "⏳"
            )
            discarded = " (已废弃)" if match.discarded else ""
            html_parts.append(
                f'<li style="margin: 5px 0;">{status} <a class="text-primary-600 dark:text-primary-500" href="/admin/main/match/{match.id}/change/">#{match.id} - {match.name}</a>{discarded}</li>'
            )

        total_count = Match.objects.filter(
            Q(applicant1=obj) | Q(applicant2=obj)
        ).count()
        if total_count > 20:
            html_parts.append(
                f'<li style="margin: 5px 0; color: #666;">... 及其他 {total_count - 20} 组</li>'
            )
        html_parts.append("</ul>")
        return format_html("".join(html_parts))

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("wechat_info", "payment")

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return self.common_readonly_fields

    def get_exclude(self, request, obj):
        return (
            []
            if request.user.is_superuser
            else [
                "mbti_ei",
                "mbti_sn",
                "mbti_tf",
                "mbti_jp",
                "hobbies",
                "fav_movies",
                "wish",
                "weekend_arrangement",
                "reply_frequency",
                "expectation",
                "preferred_sex",
                "preferred_grades",
                "preferred_schools",
                "preferred_mbti_ei",
                "preferred_mbti_sn",
                "preferred_mbti_tf",
                "preferred_mbti_jp",
            ]
        )


class WechatInfoHasAppliedFilter(admin.SimpleListFilter):
    title = "是否提交申请"
    parameter_name = "has_applied"

    def lookups(self, request, model_admin):
        return [
            ("True", "已提交"),
            ("False", "未提交"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(applicant__isnull=False)
        if self.value() == "False":
            return queryset.filter(applicant__isnull=True)
        return queryset


@admin.register(WeChatInfo)
class WeChatInfoAdmin(ModelAdmin):
    search_fields = ["nickname", "openid", "unionid"]
    readonly_fields = ["head_image_large", "created_at", "get_applicant_link"]
    list_display = ["nickname", "head_image_tag", "get_applicant_name", "created_at"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "nickname",
                    "head_image_large",
                    "get_applicant_link",
                    "created_at",
                )
            },
        ),
    )
    ordering = ["-created_at"]
    list_filter = [WechatInfoHasAppliedFilter, "created_at"]
    date_hierarchy = "created_at"

    def get_list_display_links(self, request, list_display):
        return list_display

    def get_exclude(self, request, obj):
        return [] if request.user.is_superuser else ["openid", "unionid"]

    def get_fieldsets(self, request, obj):
        fieldsets = super().get_fieldsets(request, obj)
        if request.user.is_superuser:
            fieldsets += (("Additional Info", {"fields": ("openid", "unionid")}),)
        return fieldsets

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("applicant")

    @admin.display(description="申请人姓名", ordering="applicant__name")
    def get_applicant_name(self, obj):
        if hasattr(obj, "applicant"):
            return obj.applicant.name
        return "-"

    @admin.display(description="申请人", ordering="applicant__name")
    def get_applicant_link(self, obj):
        if hasattr(obj, "applicant"):
            return format_html(
                '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/applicant/{}/change/">{}</a>',
                obj.applicant.id,
                obj.applicant.name,
            )

        return "-"

    @admin.display(description="头像")
    def head_image_tag(self, obj):
        if obj.head_image_url:
            return format_html(
                '<img src="{}" width="100" height="100" />', obj.head_image_url
            )

        return "无头像"

    @admin.display(description="头像")
    def head_image_large(self, obj):
        if obj.head_image_url:
            return format_html(
                '<img src="{}" width="150" height="150" />', obj.head_image_url
            )
        return "无头像"


@admin.register(PaymentRecord)
class PaymentRecordAdmin(ModelAdmin):
    search_fields = [
        "applicant__name",
        "applicant__wxid",
        "applicant__wechat_info__nickname",
        "transaction_id",
        "out_trade_no",
        "handle_by",
    ]
    list_display = [
        "get_applicant_name",
        "get_applicant_school",
        "get_applicant_wxid",
        "transaction_id",
        "handle_by",
        "created_at",
    ]
    list_filter = [
        "handle_by",
    ]
    readonly_fields = [
        "id",
        "applicant",
        "get_applicant_link",
        "created_at",
    ]
    fieldsets = (
        (
            "付款信息",
            {
                "fields": (
                    "id",
                    "get_applicant_link",
                    ("transaction_id", "out_trade_no"),
                    "handle_by",
                )
            },
        ),
        (
            "时间戳",
            {"fields": ("created_at",)},
        ),
    )
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("applicant", "applicant__wechat_info")
        )

    def get_fields(self, request, obj):
        return (
            [
                "id",
                "get_applicant_link",
                "transaction_id",
                "out_trade_no",
                "handle_by",
                "created_at",
            ]
            if request.user.is_superuser
            else []
        )

    @admin.display(description="申请人", ordering="applicant__name")
    def get_applicant_name(self, obj):
        if hasattr(obj, "applicant"):
            return obj.applicant.name
        return "-"

    @admin.display(description="学校", ordering="applicant__school")
    def get_applicant_school(self, obj):
        if hasattr(obj, "applicant"):
            return obj.applicant.school
        return "-"

    @admin.display(description="微信号", ordering="applicant__wxid")
    def get_applicant_wxid(self, obj):
        if hasattr(obj, "applicant"):
            return obj.applicant.wxid
        return "-"

    @admin.display(description="申请人链接")
    def get_applicant_link(self, obj):
        if hasattr(obj, "applicant"):
            return format_html(
                '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/applicant/{}/change/">{} - {}</a>',
                obj.applicant.id,
                obj.applicant.name,
                obj.applicant.school,
            )
        return "-"


class MentorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Mentor
        fields = ("username", "email", "name", "wechat", "wechat_qrcode")


class MentorChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Mentor
        fields = ("username", "email", "name", "wechat", "wechat_qrcode")


@admin.register(Mentor)
class MentorAdmin(UserAdmin):
    add_form = MentorCreationForm
    form = MentorChangeForm
    model = Mentor
    list_display = [
        "username",
        "name",
        "wechat",
        "get_match_count",
        "is_staff",
        "is_active",
        "date_joined",
    ]
    list_filter = ["is_staff", "is_active", "date_joined"]
    readonly_fields = [
        "id",
        "date_joined",
        "last_login",
        "get_qrcode_preview",
        "get_matches_list",
    ]
    fieldsets = (
        (None, {"fields": ("id", "username", "password")}),
        (
            "个人信息",
            {"fields": ("name", "wechat", "wechat_qrcode", "get_qrcode_preview")},
        ),
        (
            "管理的CP组",
            {"fields": ("get_matches_list",)},
        ),
        (
            "权限",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "时间戳",
            {"fields": (("date_joined", "last_login"),)},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "name",
                    "wechat",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("username", "name", "wechat")
    ordering = ("username",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("matches")

    @admin.display(description="管理的CP组数量")
    def get_match_count(self, obj):
        return obj.matches.count()

    @admin.display(description="微信二维码预览")
    def get_qrcode_preview(self, obj):
        if obj.wechat_qrcode:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; border: 1px solid #ddd; border-radius: 4px; padding: 5px;" />',
                obj.wechat_qrcode.url,
            )
        return "未上传二维码"

    @admin.display(description="管理的CP组列表")
    def get_matches_list(self, obj):
        matches = obj.matches.filter(discarded=False)[:20]
        if not matches:
            return "暂无分配的CP组"
        html_parts = ['<ul style="list-style: none; padding: 0;">']
        for match in matches:
            html_parts.append(
                f'<li style="margin: 5px 0;"><a class="text-primary-600 dark:text-primary-500" href="/admin/main/match/{match.id}/change/">#{match.id} - {match.name}</a></li>'
            )
        if obj.matches.filter(discarded=False).count() > 20:
            html_parts.append(
                f'<li style="margin: 5px 0; color: #666;">... 及其他 {obj.matches.filter(discarded=False).count() - 20} 组</li>'
            )
        html_parts.append("</ul>")
        return format_html("".join(html_parts))

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_staff = True
        super().save_model(request, obj, form, change)


class MatchSuccessFilter(admin.SimpleListFilter):
    title = "已成功匹配"
    parameter_name = "has_matched"

    def lookups(self, request, model_admin):
        return [
            ("True", "已成功"),
            ("False", "未成功"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(applicant1_status="A", applicant2_status="A")
        if self.value() == "False":
            return queryset.exclude(applicant1_status="A", applicant2_status="A")
        return queryset


class MatchRoundFilter(admin.SimpleListFilter):
    title = "轮次"
    parameter_name = "round"

    def lookups(self, request, model_admin):
        return [
            ("1", "第一轮"),
            ("2", "第二轮"),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(round=int(self.value()))
        return queryset


@admin.register(Match)
class MatchAdmin(ModelAdmin):
    list_display = [
        "id",
        "name",
        "get_applicant1_name",
        "get_applicant2_name",
        "get_applicant1_haspaid",
        "get_applicant2_haspaid",
        "get_confirmed",
        "get_round",
        "discarded",
        "get_mentor_name",
        "get_total_score",
    ]
    ordering = ["discarded", "id"]
    list_display_links = list_display
    search_fields = [
        "id",
        "name",
        "applicant1__name",
        "applicant2__name",
        "applicant1__wxid",
        "applicant2__wxid",
    ]
    readonly_fields = [
        "id",
        "get_applicant1_wxid",
        "get_applicant2_wxid",
        "get_applicant1_haspaid",
        "get_applicant2_haspaid",
        "get_applicant1_link",
        "get_applicant2_link",
        "get_total_score",
        "created_at",
        "updated_at",
    ]
    fieldsets = (
        (
            "配对信息",
            {"fields": ("id", "name", ("mentor", "round"))},
        ),
        (
            "嘉宾1号信息",
            {
                "fields": (
                    "get_applicant1_link",
                    ("applicant1", "get_applicant1_wxid"),
                    (
                        "applicant1_status",
                        "get_applicant1_haspaid",
                    ),
                )
            },
        ),
        (
            "嘉宾2号信息",
            {
                "fields": (
                    "get_applicant2_link",
                    ("applicant2", "get_applicant2_wxid"),
                    (
                        "applicant2_status",
                        "get_applicant2_haspaid",
                    ),
                )
            },
        ),
        (
            "状态",
            {"fields": ("discarded", "discard_reason", "get_total_score")},
        ),
        (
            "时间戳",
            {"fields": (("created_at", "updated_at"),)},
        ),
    )
    autocomplete_fields = ["applicant1", "applicant2", "mentor"]
    date_hierarchy = "created_at"

    def get_list_filter(self, request):
        return (
            [
                MatchSuccessFilter,
                "discarded",
                MatchRoundFilter,
                "mentor__name",
            ]
            if request.user.is_superuser
            else [MatchSuccessFilter, "discarded", MatchRoundFilter]
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(mentor=request.user).filter(discarded=False)
        qs = qs.select_related(
            "applicant1",
            "applicant2",
            "mentor",
            "applicant1__payment",
            "applicant2__payment",
        ).prefetch_related("tasks")
        return qs

    @admin.display(description="嘉宾1", ordering="applicant1__name")
    def get_applicant1_name(self, obj):
        return f"{obj.applicant1.name} ({obj.applicant1.school})"

    @admin.display(description="嘉宾2", ordering="applicant2__name")
    def get_applicant2_name(self, obj):
        return f"{obj.applicant2.name} ({obj.applicant2.school})"

    @admin.display(description="轮次", ordering="round")
    def get_round(self, obj):
        return Match.ROUNDS.get(obj.round, obj.round)

    @admin.display(
        description="嘉宾1已支付",
        boolean=True,
    )
    def get_applicant1_haspaid(self, obj):
        return obj.applicant1.payment is not None

    @admin.display(
        description="嘉宾2已支付",
        boolean=True,
    )
    def get_applicant2_haspaid(self, obj):
        return obj.applicant2.payment is not None

    @admin.display(description="嘉宾1微信ID", ordering="applicant1__wxid")
    def get_applicant1_wxid(self, obj):
        return obj.applicant1.wxid

    @admin.display(description="嘉宾2微信ID", ordering="applicant2__wxid")
    def get_applicant2_wxid(self, obj):
        return obj.applicant2.wxid

    @admin.display(description="嘉宾1详情")
    def get_applicant1_link(self, obj):
        return format_html(
            '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/applicant/{}/change/">{} - {} - {}</a>',
            obj.applicant1.id,
            obj.applicant1.name,
            obj.applicant1.school,
            obj.applicant1.wxid,
        )

    @admin.display(description="嘉宾2详情")
    def get_applicant2_link(self, obj):
        return format_html(
            '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/applicant/{}/change/">{} - {} - {}</a>',
            obj.applicant2.id,
            obj.applicant2.name,
            obj.applicant2.school,
            obj.applicant2.wxid,
        )

    @admin.display(description="匹配成功", boolean=True)
    def get_confirmed(self, obj):
        return obj.applicant1_status == "A" and obj.applicant2_status == "A"

    @admin.display(description="Mentor", ordering="mentor__name")
    def get_mentor_name(self, obj):
        return obj.mentor.name

    @admin.display(description="总分")
    def get_total_score(self, obj):
        return obj.total_score


class TaskCompletedFilter(admin.SimpleListFilter):
    title = "任务完成状态"
    parameter_name = "completed"

    def lookups(self, request, model_admin):
        return [
            ("completed", "已完成"),
            ("incomplete", "未完成"),
            ("has_content", "已提交内容"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "completed":
            return queryset.filter(basic_completed=True)
        if self.value() == "incomplete":
            return queryset.filter(basic_completed=False)
        if self.value() == "has_content":
            return queryset.exclude(Q(submit_text__isnull=True) | Q(submit_text=""))
        return queryset


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    list_display = [
        "get_match_info",
        "day",
        "basic_completed",
        "basic_score",
        "bonus_score",
        "daily_score",
        "get_total_score",
        "get_image_count",
        "get_updated_by",
        "updated_at",
    ]
    list_filter = [
        TaskCompletedFilter,
        "basic_completed",
        "day",
        "match__discarded",
    ]
    search_fields = [
        "match__id",
        "match__name",
        "match__applicant1__name",
        "match__applicant2__name",
        "submit_text",
    ]
    autocomplete_fields = ["match", "updated_by"]
    date_hierarchy = "created_at"
    ordering = ["-updated_at"]

    def get_readonly_fields(self, request, obj=None):
        # When creating a new task, allow match selection
        # When editing, make it readonly
        if obj:  # Editing existing task
            return [
                "id",
                "match",
                "created_at",
                "updated_at",
                "get_match_link",
                "get_images_display",
                "get_total_score",
            ]
        else:  # Creating new task
            return [
                "id",
                "created_at",
                "updated_at",
                "get_images_display",
                "get_total_score",
            ]

    def get_fieldsets(self, request, obj=None):
        if obj:  # Editing existing task
            return (
                (
                    "任务信息",
                    {
                        "fields": (
                            "id",
                            ("get_match_link", "day"),
                            "updated_by",
                            "submit_text",
                        )
                    },
                ),
                (
                    "图片",
                    {"fields": ("get_images_display",)},
                ),
                (
                    "评分",
                    {
                        "fields": (
                            "basic_completed",
                            ("basic_score", "bonus_score", "daily_score"),
                            "get_total_score",
                        )
                    },
                ),
                (
                    "时间戳",
                    {"fields": (("created_at", "updated_at"),)},
                ),
            )
        else:  # Creating new task
            return (
                (
                    "任务信息",
                    {
                        "fields": (
                            ("match", "day"),
                            "updated_by",
                            "submit_text",
                        )
                    },
                ),
                (
                    "评分",
                    {
                        "fields": (
                            "basic_completed",
                            ("basic_score", "bonus_score", "daily_score"),
                        )
                    },
                ),
            )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "match", "match__applicant1", "match__applicant2", "updated_by"
            )
            .prefetch_related("imgs")
        )

    @admin.display(description="CP组", ordering="match__id")
    def get_match_info(self, obj):
        return f"#{obj.match.id} - {obj.match.name}"

    @admin.display(description="CP组链接")
    def get_match_link(self, obj):
        return format_html(
            '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/match/{}/change/">#{} - {}</a>',
            obj.match.id,
            obj.match.id,
            obj.match.name,
        )

    @admin.display(description="总分")
    def get_total_score(self, obj):
        return obj.basic_score + obj.bonus_score + obj.daily_score

    @admin.display(description="图片数量")
    def get_image_count(self, obj):
        return obj.imgs.filter(deleted=False).count()

    @admin.display(description="最后提交者", ordering="updated_by__name")
    def get_updated_by(self, obj):
        if obj.updated_by:
            return obj.updated_by.name
        return "-"

    @admin.display(description="提交的图片")
    def get_images_display(self, obj):
        images = obj.imgs.filter(deleted=False)
        if not images:
            return "无图片"
        html_parts = []
        for img in images:
            html_parts.append(
                f'<div style="margin: 10px 0;"><img src="{img.image.url}" style="max-width: 300px; max-height: 300px; border: 1px solid #ddd; border-radius: 4px; padding: 5px;"/></div>'
            )
        return format_html("".join(html_parts))


class ImageDeletedFilter(admin.SimpleListFilter):
    title = "删除状态"
    parameter_name = "deleted"

    def lookups(self, request, model_admin):
        return [
            ("active", "未删除"),
            ("deleted", "已删除"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "active":
            return queryset.filter(deleted=False)
        if self.value() == "deleted":
            return queryset.filter(deleted=True)
        return queryset


@admin.register(Image)
class ImageAdmin(ModelAdmin):
    list_display = [
        "get_thumbnail",
        "get_match_info",
        "get_day",
        "deleted",
        "created_at",
    ]
    list_filter = [
        ImageDeletedFilter,
        "task__day",
    ]
    search_fields = [
        "task__match__id",
        "task__match__name",
        "task__match__applicant1__name",
        "task__match__applicant2__name",
    ]
    autocomplete_fields = ["task"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    def get_readonly_fields(self, request, obj=None):
        # When creating a new image, allow task selection
        # When editing, make it readonly
        if obj:  # Editing existing image
            return [
                "id",
                "task",
                "get_task_link",
                "get_match_link",
                "image_preview",
                "created_at",
            ]
        else:  # Creating new image
            return [
                "id",
                "created_at",
                "image_preview",
            ]

    def get_fieldsets(self, request, obj=None):
        if obj:  # Editing existing image
            return (
                (
                    "图片信息",
                    {
                        "fields": (
                            "id",
                            "get_task_link",
                            "get_match_link",
                            "image_preview",
                            "deleted",
                        )
                    },
                ),
                (
                    "时间戳",
                    {"fields": ("created_at",)},
                ),
            )
        else:  # Creating new image
            return (
                (
                    "图片信息",
                    {
                        "fields": (
                            "task",
                            "image",
                            "deleted",
                        )
                    },
                ),
            )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("task", "task__match")

    @admin.display(description="缩略图")
    def get_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url,
            )
        return "无图片"

    @admin.display(description="图片预览")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 500px; max-height: 500px; border: 1px solid #ddd; border-radius: 4px; padding: 5px;" />',
                obj.image.url,
            )
        return "无图片"

    @admin.display(description="CP组", ordering="task__match__id")
    def get_match_info(self, obj):
        return f"#{obj.task.match.id} - {obj.task.match.name}"

    @admin.display(description="任务天数", ordering="task__day")
    def get_day(self, obj):
        return f"第{obj.task.day}天"

    @admin.display(description="所属任务")
    def get_task_link(self, obj):
        return format_html(
            '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/task/{}/change/">第{}天 - #{} - {}</a>',
            obj.task.id,
            obj.task.day,
            obj.task.match.id,
            obj.task.match.name,
        )

    @admin.display(description="所属CP组")
    def get_match_link(self, obj):
        return format_html(
            '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/match/{}/change/">#{} - {}</a>',
            obj.task.match.id,
            obj.task.match.id,
            obj.task.match.name,
        )


class MissionTypeFilter(admin.SimpleListFilter):
    title = "任务类型"
    parameter_name = "mission_type"

    def lookups(self, request, model_admin):
        return [
            ("daily", "每日任务 (1-7)"),
            ("secret", "秘密任务 (91-94)"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "daily":
            return queryset.filter(day__lte=7)
        if self.value() == "secret":
            return queryset.filter(day__gte=91)
        return queryset


@admin.register(Mission)
class MissionAdmin(ModelAdmin):
    list_display = [
        "get_day_display",
        "title",
        "has_content",
        "has_link",
        "updated_at",
    ]
    list_filter = [MissionTypeFilter]
    search_fields = ["title", "content"]
    readonly_fields = ["id", "created_at", "updated_at"]
    fieldsets = (
        (
            "任务信息",
            {
                "fields": (
                    "id",
                    "day",
                    "title",
                    "content",
                    "link",
                )
            },
        ),
        (
            "时间戳",
            {"fields": (("created_at", "updated_at"),)},
        ),
    )
    ordering = ["day"]

    @admin.display(description="任务类型", ordering="day")
    def get_day_display(self, obj):
        return Mission.DAY.get(obj.day, f"未知任务({obj.day})")

    @admin.display(description="有内容", boolean=True)
    def has_content(self, obj):
        return bool(obj.content)

    @admin.display(description="有链接", boolean=True)
    def has_link(self, obj):
        return bool(obj.link)


class TokenHasApplicantFilter(admin.SimpleListFilter):
    title = "是否已申请"
    parameter_name = "has_applicant"

    def lookups(self, request, model_admin):
        return [
            ("yes", "已申请"),
            ("no", "未申请"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(wechat_info__applicant__isnull=False)
        if self.value() == "no":
            return queryset.filter(wechat_info__applicant__isnull=True)
        return queryset


@admin.register(Token)
class TokenAdmin(ModelAdmin):
    list_display = [
        "get_nickname",
        "get_token_short",
        "get_has_applicant",
        "created_at",
    ]
    list_filter = [TokenHasApplicantFilter, "created_at"]
    search_fields = [
        "wechat_info__nickname",
        "wechat_info__openid",
        "token",
    ]
    readonly_fields = [
        "id",
        "token",
        "wechat_info",
        "get_wechat_link",
        "get_applicant_link",
        "created_at",
    ]
    autocomplete_fields = ["wechat_info"]
    fieldsets = (
        (
            "Token信息",
            {
                "fields": (
                    "id",
                    "token",
                    "get_wechat_link",
                    "get_applicant_link",
                )
            },
        ),
        (
            "时间戳",
            {"fields": ("created_at",)},
        ),
    )
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("wechat_info")

    @admin.display(description="微信昵称", ordering="wechat_info__nickname")
    def get_nickname(self, obj):
        return obj.wechat_info.nickname

    @admin.display(description="Token (前8位)")
    def get_token_short(self, obj):
        return str(obj.token)[:8] + "..."

    @admin.display(description="已申请", boolean=True)
    def get_has_applicant(self, obj):
        return hasattr(obj.wechat_info, "applicant")

    @admin.display(description="微信信息")
    def get_wechat_link(self, obj):
        return format_html(
            '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/wechatinfo/{}/change/">{}</a>',
            obj.wechat_info.openid,
            obj.wechat_info.nickname,
        )

    @admin.display(description="关联申请人")
    def get_applicant_link(self, obj):
        if hasattr(obj.wechat_info, "applicant"):
            applicant = obj.wechat_info.applicant
            return format_html(
                '<a class="text-primary-600 dark:text-primary-500" href="/admin/main/applicant/{}/change/">{}</a>',
                applicant.id,
                applicant.name,
            )
        return "-"

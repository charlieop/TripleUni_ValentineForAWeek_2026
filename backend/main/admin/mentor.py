from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.html import format_html

from ..models import Mentor


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

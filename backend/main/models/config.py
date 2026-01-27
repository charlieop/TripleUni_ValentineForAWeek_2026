from django.db import models
from django.core.cache import cache
from datetime import datetime
from zoneinfo import ZoneInfo

_DEFAULT_TIMSZONE_STRING = "Asia/Shanghai"
_DEFAULT_TIMEZONE = ZoneInfo(_DEFAULT_TIMSZONE_STRING)
_DEFAULT_MAINTENANCE_MODE = False
_DEFAULT_MAINTENANCE_END = datetime(
    year=2026, month=2, day=28, hour=23, minute=59, second=59, tzinfo=_DEFAULT_TIMEZONE
)
_DEFAULT_DEBUG = False

# Default activity dates
_DEFAULT_APPLICATION_START = datetime(
    year=2026, month=1, day=31, hour=19, minute=0, second=0, tzinfo=_DEFAULT_TIMEZONE
)
_DEFAULT_APPLICATION_END = datetime(
    year=2026, month=2, day=6, hour=0, minute=30, second=0, tzinfo=_DEFAULT_TIMEZONE
)
_DEFAULT_FIRST_MATCH_RESULT_RELEASE = datetime(
    year=2026, month=2, day=6, hour=6, minute=0, second=0, tzinfo=_DEFAULT_TIMEZONE
)
_DEFAULT_FIRST_MATCH_CONFIRM_END = datetime(
    year=2026, month=2, day=7, hour=6, minute=5, second=0, tzinfo=_DEFAULT_TIMEZONE
)
_DEFAULT_SECOND_MATCH_RESULT_RELEASE = datetime(
    year=2026, month=2, day=7, hour=12, minute=0, second=0, tzinfo=_DEFAULT_TIMEZONE
)
_DEFAULT_ACTIVITY_START = datetime(
    year=2026, month=2, day=7, hour=22, minute=0, second=0, tzinfo=_DEFAULT_TIMEZONE
)
_DEFAULT_FIRST_MISSION_RELEASE = datetime(
    year=2026, month=2, day=8, hour=0, minute=0, second=0, tzinfo=_DEFAULT_TIMEZONE
)
_DEFAULT_FIRST_MISSION_END = datetime(
    year=2026, month=2, day=9, hour=6, minute=5, second=0, tzinfo=_DEFAULT_TIMEZONE
)
_DEFAULT_EXIT_QUESTIONNAIRE_RELEASE = datetime(
    year=2026, month=2, day=14, hour=6, minute=0, second=0, tzinfo=_DEFAULT_TIMEZONE
)
_DEFAULT_EXIT_QUESTIONNAIRE_END = datetime(
    year=2026, month=2, day=17, hour=0, minute=30, second=0, tzinfo=_DEFAULT_TIMEZONE
)

class Config(models.Model):
    """
    Singleton model to store application configuration.
    Only one instance of this model should exist.
    """

    # Maintenance
    maintenance_mode = models.BooleanField(
        default=_DEFAULT_MAINTENANCE_MODE, verbose_name="维护模式", help_text="启用后，系统将进入维护模式"
    )
    expected_maintenance_end = models.DateTimeField(
        default=_DEFAULT_MAINTENANCE_END,
        verbose_name="预计维护结束时间",
        help_text="维护预计结束的时间",
    )

    # Debug Mode
    debug_mode = models.BooleanField(
        default=_DEFAULT_DEBUG, verbose_name="调试模式", help_text="启用后，将跳过时间段验证"
    )

    # Time Zone
    timezone = models.CharField(
        max_length=50,
        default=_DEFAULT_TIMSZONE_STRING,
        verbose_name="时区",
        help_text="应用程序使用的时区，例如: America/New_York, Asia/Shanghai",
    )

    # Application Period
    application_start = models.DateTimeField(
        default=_DEFAULT_APPLICATION_START,
        verbose_name="申请开始时间", help_text="用户可以开始提交申请的时间"
    )
    application_end = models.DateTimeField(
        default=_DEFAULT_APPLICATION_END,
        verbose_name="申请结束时间", help_text="申请截止时间"
    )

    # First Match
    first_match_result_release = models.DateTimeField(
        default=_DEFAULT_FIRST_MATCH_RESULT_RELEASE,
        verbose_name="第一轮匹配结果发布时间", help_text="第一轮匹配结果公布的时间"
    )
    first_match_confirm_end = models.DateTimeField(
        default=_DEFAULT_FIRST_MATCH_CONFIRM_END,
        verbose_name="第一轮匹配确认截止时间", help_text="第一轮匹配确认的截止时间"
    )

    # Second Match
    second_match_result_release = models.DateTimeField(
        default=_DEFAULT_SECOND_MATCH_RESULT_RELEASE,
        verbose_name="第二轮匹配结果发布时间", help_text="第二轮匹配结果公布的时间"
    )

    # Activity Period
    activity_start = models.DateTimeField(
        default=_DEFAULT_ACTIVITY_START,
        verbose_name="活动开始时间", help_text="活动正式开始的时间"
    )

    # Mission Period
    first_mission_release = models.DateTimeField(
        default=_DEFAULT_FIRST_MISSION_RELEASE,
        verbose_name="第一个任务发布时间", help_text="第一天任务发布的时间"
    )
    first_mission_end = models.DateTimeField(
        default=_DEFAULT_FIRST_MISSION_END,
        verbose_name="第一个任务截止时间", help_text="第一天任务提交的截止时间"
    )

    # Exit Questionnaire
    exit_questionnaire_release = models.DateTimeField(
        default=_DEFAULT_EXIT_QUESTIONNAIRE_RELEASE,
        verbose_name="退出问卷发布时间", help_text="退出问卷开放的时间"
    )
    exit_questionnaire_end = models.DateTimeField(
        default=_DEFAULT_EXIT_QUESTIONNAIRE_END,
        verbose_name="退出问卷截止时间", help_text="退出问卷关闭的时间"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "系统配置"
        verbose_name_plural = "系统配置"

    def save(self, *args, **kwargs):
        """
        Ensure only one Config instance exists (singleton pattern).
        Clear cache after saving to ensure real-time updates.
        """
        self.pk = 1
        super().save(*args, **kwargs)
        # Clear the cache to force reload of config
        cache.delete("app_config")

    def delete(self, *args, **kwargs):
        """Prevent deletion of the config instance."""
        pass

    @classmethod
    def load(cls):
        """
        Load the config instance with caching for performance.
        Cache timeout is set to 5 seconds for near real-time updates.
        Returns None if the table doesn't exist yet (during migrations).
        """
        config = cache.get("app_config")
        if config is None:
            try:
                config, created = cls.objects.get_or_create(pk=1)
                cache.set("app_config", config, timeout=None)
            except Exception:
                # Table doesn't exist yet (during migrations)
                return None
        return config

    def __str__(self):
        return f"系统配置 (更新于 {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')})"

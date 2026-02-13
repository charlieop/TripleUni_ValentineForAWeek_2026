from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from rest_framework.exceptions import ValidationError
from .models import Config
def get_config():
    """
    Get the Config instance. Import here to avoid circular imports.
    This function is cached in the Config.load() method for performance.
    """
    return Config.load()


def __getattr__(name):
    """
    Module-level __getattr__ to dynamically fetch config values.
    This allows accessing MAINTENANCE_MODE and EXPECTED_MAINTENANCE_END
    as module-level variables while fetching them dynamically from the database.
    """
    if name == "MAINTENANCE_MODE":
        config = get_config()
        return config.maintenance_mode
    elif name == "EXPECTED_MAINTENANCE_END":
        config = get_config()
        return config.expected_maintenance_end
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


class _ConfigMeta(type):
    """
    Metaclass to dynamically fetch config values as class attributes.
    """

    @property
    def TIME_ZONE(cls):
        """Get the timezone from config."""
        config = get_config()
        return ZoneInfo(config.timezone)

    @property
    def APPLICATION_START(cls):
        """Get application start time from config."""
        config = get_config()
        return config.application_start

    @property
    def APPLICATION_END(cls):
        """Get application end time from config."""
        config = get_config()
        return config.application_end

    @property
    def FIRST_MATCH_RESULT_RELEASE(cls):
        """Get first match result release time from config."""
        config = get_config()
        return config.first_match_result_release

    @property
    def FIRST_MATCH_CONFIRM_END(cls):
        """Get first match confirmation end time from config."""
        config = get_config()
        return config.first_match_confirm_end

    @property
    def SECOND_MATCH_RESULT_RELEASE(cls):
        """Get second match result release time from config."""
        config = get_config()
        return config.second_match_result_release

    @property
    def ACTIVITY_START(cls):
        """Get activity start time from config."""
        config = get_config()
        return config.activity_start

    @property
    def FIRST_MISSION_RELEASE(cls):
        """Get first mission release time from config."""
        config = get_config()
        return config.first_mission_release

    @property
    def FIRST_MISSION_END(cls):
        """Get first mission end time from config."""
        config = get_config()
        return config.first_mission_end

    @property
    def EXIT_QUESTIONNAIRE_RELEASE(cls):
        """Get exit questionnaire release time from config."""
        config = get_config()
        return config.exit_questionnaire_release

    @property
    def EXIT_QUESTIONNAIRE_END(cls):
        """Get exit questionnaire end time from config."""
        config = get_config()
        return config.exit_questionnaire_end

    @property
    def DEBUG(cls):
        """Get debug mode status from config."""
        config = get_config()
        return config.debug_mode


class AvtivityDates(metaclass=_ConfigMeta):
    """
    Configuration class for activity dates and periods.
    All values are dynamically loaded from the database Config model.
    Uses a metaclass to provide class-level properties that fetch from the database.
    """

    @staticmethod
    def MISSION_RELEASE_DAY(day: int):
        """Calculate mission release day based on the first mission release."""
        return AvtivityDates.FIRST_MISSION_RELEASE + timedelta(days=day - 1)

    @staticmethod
    def MISSION_SUBMIT_END_DAY(day: int):
        """Calculate mission submission end day based on the first mission end."""
        return AvtivityDates.FIRST_MISSION_END + timedelta(days=day - 1)

    @staticmethod
    def now() -> datetime:
        """Get current datetime in the configured timezone."""
        config = get_config()
        return datetime.now(ZoneInfo(config.timezone))

    @staticmethod
    def has_passed(date: datetime) -> bool:
        """Check if a given datetime has passed."""
        return date <= AvtivityDates.now()

    @staticmethod
    def assert_valid_application_period():
        """Validate that current time is within application period."""
        if AvtivityDates.DEBUG:
            return
        if not AvtivityDates.has_passed(AvtivityDates.APPLICATION_START):
            raise ValidationError({"detail": "Application has not started yet"})
        elif AvtivityDates.has_passed(AvtivityDates.APPLICATION_END):
            raise ValidationError({"detail": "Application has ended"})

    @staticmethod
    def assert_valid_view_match_result_period():
        """Validate that match results can be viewed."""
        if AvtivityDates.DEBUG:
            return
        if not AvtivityDates.has_passed(AvtivityDates.FIRST_MATCH_RESULT_RELEASE):
            raise ValidationError({"detail": "Match result has not been released yet"})

    @staticmethod
    def assert_valid_set_match_result_period():
        """Validate that match results can be confirmed."""
        if AvtivityDates.DEBUG:
            return
        if not AvtivityDates.has_passed(AvtivityDates.FIRST_MATCH_RESULT_RELEASE):
            raise ValidationError({"detail": "Match result has not been released yet"})
        elif AvtivityDates.has_passed(AvtivityDates.FIRST_MATCH_CONFIRM_END):
            raise ValidationError(
                {"detail": "The match result confirmation period has ended"}
            )

    @staticmethod
    def assert_valid_view_match_detail_period():
        """Validate that match details can be viewed."""
        if AvtivityDates.DEBUG:
            return
        if not AvtivityDates.has_passed(AvtivityDates.ACTIVITY_START):
            raise ValidationError({"detail": "Activity has not started yet"})

    @staticmethod
    def assert_valid_set_match_detail_period():
        """Validate that match details can be modified."""
        if AvtivityDates.DEBUG:
            return
        if not AvtivityDates.has_passed(AvtivityDates.ACTIVITY_START):
            raise ValidationError({"detail": "Activity has not started yet"})
        elif AvtivityDates.has_passed(AvtivityDates.EXIT_QUESTIONNAIRE_END):
            raise ValidationError({"detail": "The activity has ended"})

    @staticmethod
    def assert_valid_view_task_period(day: int):
        """Validate that task for a specific day can be viewed."""
        if AvtivityDates.DEBUG:
            return
        if not AvtivityDates.has_passed(AvtivityDates.MISSION_RELEASE_DAY(day)):
            raise ValidationError({"detail": "Mission has not been released yet"})

    @staticmethod
    def assert_valid_exit_questionnaire_period():
        """Validate that current time is within exit questionnaire period."""
        if AvtivityDates.DEBUG:
            return
        if not AvtivityDates.has_passed(AvtivityDates.EXIT_QUESTIONNAIRE_RELEASE):
            raise ValidationError(
                {"detail": "Exit questionnaire has not been released yet"}
            )
        elif AvtivityDates.has_passed(AvtivityDates.EXIT_QUESTIONNAIRE_END):
            raise ValidationError(
                {"detail": "Exit questionnaire submission has ended"}
            )

    @staticmethod
    def assert_valid_set_task_period(day: int):
        """Validate that task for a specific day can be submitted."""
        if AvtivityDates.DEBUG:
            return
        if not AvtivityDates.has_passed(AvtivityDates.MISSION_RELEASE_DAY(day)):
            raise ValidationError(
                {"detail": f"Task for day {day} has not been released yet"}
            )
        elif AvtivityDates.has_passed(AvtivityDates.MISSION_SUBMIT_END_DAY(day)):
            raise ValidationError(
                {"detail": f"The task submission period for day {day} has ended"}
            )

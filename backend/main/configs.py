from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from rest_framework.exceptions import ValidationError


# Configuration for the application
class AvtivityDates:

    # XXX: TODO: Change this to the actual time zone
    TIME_ZONE = ZoneInfo("America/New_York")
    
    APPLICATION_START = datetime(
        year=2026, month=1, day=24, hour=14, minute=26, second=40, tzinfo=TIME_ZONE
    )
    APPLICATION_END = datetime(
        year=2026, month=1, day=24, hour=14, minute=27, second=59, tzinfo=TIME_ZONE
    )

    FIRST_MATCH_RESULT_RELEASE = datetime(
        year=2026, month=1, day=6, hour=6, minute=0, second=0, tzinfo=TIME_ZONE
    )
    FIRST_MATCH_CONFIRM_END = datetime(
        year=2026, month=2, day=7, hour=6, minute=5, second=0, tzinfo=TIME_ZONE
    )

    SECOND_MATCH_RESULT_RELEASE = datetime(
        year=2026, month=2, day=7, hour=12, minute=0, second=0, tzinfo=TIME_ZONE
    )

    ACTIVITY_START = datetime(
        year=2026, month=2, day=7, hour=22, minute=0, second=0, tzinfo=TIME_ZONE
    )

    FIRST_MISSION_RELEASE = datetime(
        year=2026, month=2, day=8, hour=0, minute=0, second=0, tzinfo=TIME_ZONE
    )
    FIRST_MISSION_END = datetime(
        year=2026, month=2, day=9, hour=6, minute=5, second=0, tzinfo=TIME_ZONE
    )

    EXIT_QUESTIONNAIRE_RELEASE = datetime(
        year=2026, month=2, day=14, hour=0, minute=0, second=0, tzinfo=TIME_ZONE
    )
    EXIT_QUESTIONNAIRE_END = datetime(
        year=2026, month=2, day=16, hour=23, minute=59, second=0, tzinfo=TIME_ZONE
    )
    
    # TIME_ZONE = ZoneInfo("Asia/Shanghai")

    # APPLICATION_START = datetime(
    #     year=2026, month=2, day=1, hour=6, minute=0, second=0, tzinfo=TIME_ZONE
    # )
    # APPLICATION_END = datetime(
    #     year=2026, month=2, day=6, hour=0, minute=30, second=0, tzinfo=TIME_ZONE
    # )

    # FIRST_MATCH_RESULT_RELEASE = datetime(
    #     year=2026, month=2, day=6, hour=6, minute=0, second=0, tzinfo=TIME_ZONE
    # )
    # FIRST_MATCH_CONFIRM_END = datetime(
    #     year=2026, month=2, day=7, hour=6, minute=5, second=0, tzinfo=TIME_ZONE
    # )

    # SECOND_MATCH_RESULT_RELEASE = datetime(
    #     year=2026, month=2, day=7, hour=12, minute=0, second=0, tzinfo=TIME_ZONE
    # )

    # ACTIVITY_START = datetime(
    #     year=2026, month=2, day=7, hour=22, minute=0, second=0, tzinfo=TIME_ZONE
    # )

    # FIRST_MISSION_RELEASE = datetime(
    #     year=2026, month=2, day=8, hour=0, minute=0, second=0, tzinfo=TIME_ZONE
    # )
    # FIRST_MISSION_END = datetime(
    #     year=2026, month=2, day=9, hour=6, minute=5, second=0, tzinfo=TIME_ZONE
    # )

    # EXIT_QUESTIONNAIRE_RELEASE = datetime(
    #     year=2026, month=2, day=14, hour=0, minute=0, second=0, tzinfo=TIME_ZONE
    # )
    # EXIT_QUESTIONNAIRE_END = datetime(
    #     year=2026, month=2, day=16, hour=23, minute=59, second=0, tzinfo=TIME_ZONE
    # )
    
    @staticmethod
    def MISSION_RELEASE_DAY(day: int):
        return AvtivityDates.FIRST_MISSION_RELEASE + timedelta(days=day - 1)

    @staticmethod
    def MISSION_SUBMIT_END_DAY(day: int):
        return AvtivityDates.FIRST_MISSION_END + timedelta(days=day - 1)
    
    @staticmethod
    def now() -> datetime:
        return datetime.now(AvtivityDates.TIME_ZONE)
    
    @staticmethod
    def has_passed(date: datetime) -> bool:
        return date <= AvtivityDates.now()
    
    # XXX: TODO: Remove this before deployment
    DEBUG = False
    
    @staticmethod
    def assert_valid_application_period():
        if AvtivityDates.DEBUG:
            return
        if not AvtivityDates.has_passed(AvtivityDates.APPLICATION_START):
            raise ValidationError({"detail": "Application has not started yet"})
        elif AvtivityDates.has_passed(AvtivityDates.APPLICATION_END):
            raise ValidationError({"detail": "Application has ended"})

    @staticmethod
    def assert_valid_view_match_result_period():
        if AvtivityDates.DEBUG:
            return
        if not AvtivityDates.has_passed(AvtivityDates.FIRST_MATCH_RESULT_RELEASE):
            raise ValidationError({"detail": "Match result has not been released yet"})

    @staticmethod
    def assert_valid_set_match_result_period():
        if AvtivityDates.DEBUG:
            return
        if not AvtivityDates.has_passed(AvtivityDates.FIRST_MATCH_CONFIRM_END):
            raise ValidationError({"detail": "Match result has not been released yet"})
        elif AvtivityDates.has_passed(AvtivityDates.FIRST_MATCH_CONFIRM_END):
            raise ValidationError(
                {"detail": "The match result confirmation period has ended"}
            )

    @staticmethod
    def assert_valid_view_match_detail_period():
        if AvtivityDates.DEBUG:
            return
        if not AvtivityDates.has_passed(AvtivityDates.ACTIVITY_START):
            raise ValidationError({"detail": "Activity has not started yet"})
        
    @staticmethod
    def assert_valid_set_match_detail_period():
        if AvtivityDates.DEBUG:
            return
        if not AvtivityDates.has_passed(AvtivityDates.ACTIVITY_START):
            raise ValidationError({"detail": "Activity has not started yet"})
        elif AvtivityDates.has_passed(AvtivityDates.EXIT_QUESTIONNAIRE_END):
            raise ValidationError({"detail": "The activity has ended"})
        
    @staticmethod
    def assert_valid_view_task_period(day: int):
        if AvtivityDates.DEBUG:
            return
        if not AvtivityDates.has_passed(AvtivityDates.MISSION_RELEASE_DAY(day)):
            raise ValidationError({"detail": "Mission has not been released yet"})
    
    @staticmethod
    def assert_valid_set_task_period(day: int):
        if AvtivityDates.DEBUG:
            return
        if not AvtivityDates.has_passed(AvtivityDates.MISSION_SUBMIT_END_DAY(day)):
            raise ValidationError({"detail": f"Task for day {day} has not been released yet"})
        elif AvtivityDates.has_passed(AvtivityDates.MISSION_SUBMIT_END_DAY(day)):
            raise ValidationError({"detail": f"The task submission period for day {day} has ended"})
        
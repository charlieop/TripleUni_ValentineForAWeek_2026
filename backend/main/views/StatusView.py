from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from enum import Enum
from datetime import datetime
from rest_framework.exceptions import NotFound

from ..mixin import UtilMixin
from ..logger import CustomLogger
from ..configs import AvtivityDates

logger = CustomLogger("status")


class Status(Enum):
    NOT_STARTED = "NOT_STARTED"

    APPLICATION_START = "APPLICATION_START"
    APPLIED = "APPLIED"
    PAID = "PAID"
    APPLICATION_END = "APPLICATION_END"
    QUITTED = "QUITTED"

    WAITING_FOR_FIRST_MATCH_RESULT = "WAITING_FOR_FIRST_MATCH_RESULT"
    FIRST_MATCH_RESULT_RELEASE = "FIRST_MATCH_RESULT_RELEASE"
    FIRST_MATCH_CONFIRM_END = "FIRST_MATCH_CONFIRM_END"
    SECOND_MATCH_RESULT_RELEASE = "SECOND_MATCH_RESULT_RELEASE"

    ACTIVITY_START = "ACTIVITY_START"

    EXIT_QUESTIONNAIRE_RELEASE = "EXIT_QUESTIONNAIRE_RELEASE"
    EXIT_QUESTIONNAIRE_END = "EXIT_QUESTIONNAIRE_END"


class StatusView(APIView, UtilMixin):
    def _get_status(self, token: str) -> tuple[Status, datetime]:
        now = AvtivityDates.now()

        # Before application starts
        if now < AvtivityDates.APPLICATION_START:
            return (Status.NOT_STARTED, AvtivityDates.APPLICATION_START)

        # Try to get applicant
        try:
            applicant = self.get_applicant_by_token(token)
        except NotFound:
            return (
                (Status.APPLICATION_START, AvtivityDates.APPLICATION_END)
                if now < AvtivityDates.APPLICATION_END
                else (Status.APPLICATION_END, None)
            )

        # Check if applicant quit
        if applicant.quitted:
            return (Status.QUITTED, None)

        # During application period
        if now < AvtivityDates.APPLICATION_END:
            return (Status.PAID, AvtivityDates.APPLICATION_END) if applicant.has_paid() else (Status.APPLIED, AvtivityDates.APPLICATION_END)

        # After application period - must have paid to continue
        if not applicant.has_paid():
            return (Status.QUITTED, None)

        # Time-based status progression after application period
        status_timeline = [
            (
                AvtivityDates.FIRST_MATCH_RESULT_RELEASE,
                Status.WAITING_FOR_FIRST_MATCH_RESULT,
            ),
            (AvtivityDates.FIRST_MATCH_CONFIRM_END, Status.FIRST_MATCH_RESULT_RELEASE),
            (AvtivityDates.SECOND_MATCH_RESULT_RELEASE, Status.FIRST_MATCH_CONFIRM_END),
            (AvtivityDates.ACTIVITY_START, Status.SECOND_MATCH_RESULT_RELEASE),
        ]

        for deadline, status_value in status_timeline:
            if now < deadline:
                return (status_value, deadline)
            
        try:
            match, user_role = self.get_match_by_applicant(applicant)
        except NotFound:
            return (Status.QUITTED, None)
        if match.discarded:
            return (Status.QUITTED, None)
            
        # Time-based status progression after application period
        status_timeline = [
            (AvtivityDates.EXIT_QUESTIONNAIRE_RELEASE, Status.ACTIVITY_START),
            (AvtivityDates.EXIT_QUESTIONNAIRE_END, Status.EXIT_QUESTIONNAIRE_RELEASE),
        ]

        for deadline, status_value in status_timeline:
            if now < deadline:
                return (status_value, deadline)

        return (Status.EXIT_QUESTIONNAIRE_END, None)

    def get(self, request):
        return Response(
            {
                "data": {
                    "status": Status.APPLIED.value,
                    "deadline": AvtivityDates.APPLICATION_START.timestamp(),
                }
            },
            status=status.HTTP_200_OK,
        )
        token = self.get_token(request)
        openid = self.get_openid_by_token(token)
        status_obj, deadline = self._get_status(token)
        logger.info(f"GET: {openid}, status: {status_obj.value}")
        return Response({"data": {"status": status_obj.value, "deadline": deadline.timestamp() if deadline else None}}, status=status.HTTP_200_OK)
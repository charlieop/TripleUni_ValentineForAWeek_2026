from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from enum import Enum

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

    FIRST_MATCH_RESULT_RELEASE = "FIRST_MATCH_RESULT_RELEASE"
    FIRST_MATCH_CONFIRM_END = "FIRST_MATCH_CONFIRM_END"
    SECOND_MATCH_RESULT_RELEASE = "SECOND_MATCH_RESULT_RELEASE"

    ACTIVITY_START = "ACTIVITY_START"

    EXIT_QUESTIONNAIRE_RELEASE = "EXIT_QUESTIONNAIRE_RELEASE"
    EXIT_QUESTIONNAIRE_END = "EXIT_QUESTIONNAIRE_END"


class StatusView(APIView, UtilMixin):

    def get(self, request):

        token = self.get_token(request)
        now = AvtivityDates.now
        
        if now < AvtivityDates.APPLICATION_START:
            return Response(
                {"data": {"status": Status.NOT_STARTED.value}},
                status=status.HTTP_200_OK,
            )
            
        try:
            applicant = self.get_applicant_by_token(token)
        except NotFound:
            return Response(
                {"data": {"status": Status.APPLICATION_START.value}},
                status=status.HTTP_200_OK,
            )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from ..mixin import UtilMixin
from ..serializers.mission import MissionSerializer
from ..logger import CustomLogger
from ..configs import AvtivityDates

logger = CustomLogger("mission")


class MissionDetailView(APIView, UtilMixin):
    def get(self, request, day: int):
        # Only accessible after this day's mission is released
        AvtivityDates.assert_valid_view_task_period(day)

        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)

        match, user_role = self.get_match_by_applicant(applicant)
        self.assert_match_not_discarded(match)
        self.assert_day_valid(day)

        mission = self.get_mission_by_day(day)
        if mission is None:
            raise NotFound({"detail": f"Mission for day {day} not found"})

        logger.info(f"GET mission day {day}: {applicant.wechat_info.openid}")
        serializer = MissionSerializer(mission)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


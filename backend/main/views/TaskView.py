from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..mixin import UtilMixin
from ..serializers.task import GetTaskSerializer, SetTaskSerializer
from ..logger import CustomLogger
from ..configs import AvtivityDates

logger = CustomLogger("task")


class TaskDetailView(APIView, UtilMixin):
    def get(self, request, day):
        AvtivityDates.assert_valid_view_task_period(day)
        
        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)

        match, user_role = self.get_match_by_applicant(applicant)
        self.assert_match_not_discarded(match)
        self.assert_day_valid(day)

        task = self.get_task_by_match_and_day(match, day)
        due = AvtivityDates.now() >= AvtivityDates.MISSION_SUBMIT_END_DAY(day)

        logger.info(
            f"GET task day {day}: {applicant.wechat_info.openid}, match_id: {match.id}"
        )

        serializer = GetTaskSerializer(task, context={"due": due})
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, day):
        AvtivityDates.assert_valid_set_task_period(day)
        
        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)

        match, user_role = self.get_match_by_applicant(applicant)
        self.assert_match_not_discarded(match)
        self.assert_day_valid(day)

        task = self.get_task_by_match_and_day(match, day)
        task.updated_by = applicant

        serializer = SetTaskSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info(
            f"POST task day {day}: {applicant.wechat_info.openid}, match_id: {match.id}"
        )

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

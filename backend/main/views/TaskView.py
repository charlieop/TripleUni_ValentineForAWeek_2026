from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..mixin import UtilMixin
from ..serializers.task import (
    GetTaskSerializer,
    SetTaskSerializer,
    TaskVisibilitySerializer,
)
from ..logger import CustomLogger
from ..configs import AvtivityDates

logger = CustomLogger("task")


class SecretTaskView(APIView, UtilMixin):
    def get(self, request):
        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)

        match, user_role = self.get_match_by_applicant(applicant)
        self.assert_match_not_discarded(match)

        logger.info(
            f"Get secret task by {applicant.wechat_info.openid}, match_id: {match.id}"
        )

        title = (
            "我们的点点滴滴" if user_role == 1 else "那些被歌声保存的日子"
        )

        desc = (
            "记录每天聊天中，自己感觉最甜蜜的时刻。可以是对方戳动你的话，也可以是你觉得最有趣的互动，并且在最后一天，以任意形式分享给对方。"
            if user_role == 1
            else "每天用一首歌代表你们相处, 可以为每天相处的心情，或者给对方当天的印象，挑选一首歌，并且整理好在最后一天发给对方，回忆和表达那时的心情！"
        )

        return Response({"data": {"title": title, "desc": desc}}, status=status.HTTP_200_OK)


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


class TaskVisibilityView(APIView, UtilMixin):
    """
    Update mentor visibility for a task.
    This endpoint is available after the mission is released, and remains
    available even after the submission period has ended.
    """

    def post(self, request, day: int):
        # Only require that the mission has been released (view period),
        # do not restrict by submission end time.
        AvtivityDates.assert_valid_view_task_period(day)

        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)

        match, user_role = self.get_match_by_applicant(applicant)
        self.assert_match_not_discarded(match)
        self.assert_day_valid(day)

        task = self.get_task_by_match_and_day(match, day)

        serializer = TaskVisibilitySerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info(
            f"POST task visibility day {day}: {applicant.wechat_info.openid}, match_id: {match.id}, visible_to_mentor: {serializer.data.get('visible_to_mentor')}"
        )

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

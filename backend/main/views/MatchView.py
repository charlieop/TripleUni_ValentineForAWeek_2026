from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from ..mixin import UtilMixin
from ..models import Task, Match
from ..serializers.match import MatchResultSerializer, MatchDetailSerializer
from ..logger import CustomLogger
from ..configs import AvtivityDates

logger = CustomLogger("match")


class MatchResultDetailView(APIView, UtilMixin):
    """View for GET and POST:/match-result/<matchID> - Get match result details or update status"""

    def get(self, request):
        AvtivityDates.assert_valid_view_match_result_period()

        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)

        match, user_role = self.get_match_by_applicant(applicant)

        logger.info(
            f"GET match-result: {applicant.wechat_info.openid}, match_id: {match.id}, round: {match.round}"
        )

        other_applicant = match.applicant1 if user_role == 2 else match.applicant2

        # Prepare data for serializer
        data = {
            "match": match,
            "other_applicant": other_applicant,
            "user_role": user_role,
        }

        serializer = MatchResultSerializer(data)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        AvtivityDates.assert_valid_set_match_result_period()

        # Get new status from request
        new_status = request.data.get("status")
        if new_status not in ["A", "R"]:
            raise ValidationError(
                {"detail": "Status must be either 'A' (Accepted) or 'R' (Rejected)"}
            )

        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)

        match, user_role = self.get_match_by_applicant(applicant)

        # Check if round is 1 (users can only set status if round is 1)
        if match.round != 1:
            raise ValidationError({"detail": "Status can only be updated in round 1"})

        status_field = f"applicant{user_role}_status"
        current_status = getattr(match, status_field)

        # Check if user has already made a choice (cannot update once chosen)
        if current_status != "P":
            raise ValidationError(
                {"detail": "You have already made your choice and cannot update it"}
            )

        # Update the status
        setattr(match, status_field, new_status)
        match.save()

        # If any applicant chooses R, set match as discarded
        if new_status == "R":
            match.discarded = True
            match.discard_reason = (
                f"嘉宾 { applicant.wechat_info.nickname } 拒绝了此轮匹配"
            )
            match.save()
            logger.warning(
                f"POST match-result: {applicant.wechat_info.openid}, match_id: {match.id}, REJECTED"
            )
        else:
            logger.info(
                f"POST match-result: {applicant.wechat_info.openid}, match_id: {match.id}, status: {new_status}"
            )

        return Response(
            {"detail": "Match result updated successfully"}, status=status.HTTP_200_OK
        )


class MatchDetailView(APIView, UtilMixin):
    """View for GET and POST:/match/<matchID> - Get match details with score or update match name"""

    def get(self, request):
        AvtivityDates.assert_valid_view_match_detail_period()

        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)

        match, user_role = self.get_match_by_applicant(applicant)

        self.assert_match_not_discarded(match)

        user_applicant = match.applicant1 if user_role == 1 else match.applicant2
        other_applicant = match.applicant2 if user_role == 1 else match.applicant1

        # Calculate total score (sum of basic_score, bonus_score, daily_score of all tasks)
        tasks = Task.objects.filter(match=match)
        basic_complete = [False] * 7
        for i in range(1, 8):
            task = tasks.filter(day=i).first()
            if task and task.basic_completed:
                basic_complete[i - 1] = True

        day = (AvtivityDates.now() - AvtivityDates.FIRST_MISSION_RELEASE).days + 1
        day = max(min(day, 8), 0)

        # Get rank using the mixin method (calculates all ranks and caches for 15 minutes)
        current_score = match.total_score
        rank = self.get_rank(match.id)

        logger.info(
            f"GET match: {applicant.wechat_info.openid}, match_id: {match.id}, score: {current_score}, rank: {rank}"
        )

        # Prepare data for serializer
        data = {
            "match": match,
            "user_applicant": user_applicant,
            "other_applicant": other_applicant,
            "total_score": current_score,
            "basic_complete": basic_complete,
            "current_day": day,
            "rank": rank,
        }

        serializer = MatchDetailSerializer(data)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        AvtivityDates.assert_valid_set_match_detail_period()

        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)

        match, user_role = self.get_match_by_applicant(applicant)

        self.assert_match_not_discarded(match)

        # Get new name from request
        new_name = request.data.get("name")
        if not new_name:
            raise ValidationError({"detail": "Name is required"})

        if len(new_name) > 30:
            raise ValidationError({"detail": "Name must be 30 characters or less"})

        # Update the match name
        match.name = new_name
        match.save()

        logger.info(
            f"POST match: {applicant.wechat_info.openid}, match_id: {match.id}, new name: {new_name}"
        )

        return Response(
            {"detail": "Match name updated successfully"}, status=status.HTTP_200_OK
        )

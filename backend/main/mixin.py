from datetime import timedelta
from rest_framework.exceptions import (
    AuthenticationFailed,
    APIException,
    ParseError,
    NotFound,
    PermissionDenied,
    ValidationError,
)
from rest_framework.request import Request
import uuid
import pickle
from django.core.cache import cache
from django.db.models import Q, Sum, F, Case, When, Value, IntegerField

from . import configs
from .models import Applicant, Token, Match, WeChatInfo, Task, Mission


class Gone(APIException):
    status_code = 410
    default_detail = "The requested resource is no longer available."
    default_code = "gone"


class Conflict(APIException):
    status_code = 409
    default_detail = "A conflict occurred."
    default_code = "conflict"


class NoContent(APIException):
    status_code = 204
    default_detail = "No content"
    default_code = "no_content"


class InternalServerError(APIException):
    status_code = 500
    default_detail = "An internal server error occurred."
    default_code = "internal_server_error"


class UtilMixin:
    def get_token(self, request: Request) -> str:
        token = request.headers.get("Authorization")
        if token is None or token == "":
            raise AuthenticationFailed(
                {"detail": 'Authorization header with user "token" is required'}
            )
        if configs.MAINTENANCE_MODE:
            raise InternalServerError(
                {
                    "detail": "We are currently undergoing maintenance. Please try again later."
                }
            )
        return token

    def get_openid_by_token(self, token: str) -> str:
        cache_key = f"token:{token}:openid"
        openid = cache.get(cache_key)
        if openid is not None:
            return openid

        token_obj = Token.objects.filter(token=token).first()
        if token_obj is None:
            raise AuthenticationFailed({"detail": "Token is invalid"})
        openid = token_obj.wechat_info.openid
        cache.set(cache_key, openid, timeout=3600)  # Cache for 1 hour
        return openid

    def get_wechat_info_by_token(self, token: str) -> WeChatInfo:
        cache_key = f"token:{token}:wechat_info"
        wechat_info = cache.get(cache_key)
        if wechat_info is not None:
            return wechat_info

        token_obj = Token.objects.filter(token=token).first()
        if token_obj is None:
            raise AuthenticationFailed({"detail": "Token is invalid"})
        wechat_info = token_obj.wechat_info
        cache.set(cache_key, wechat_info, timeout=3600)  # Cache for 1 hour
        return wechat_info

    def get_applicant_by_token(self, token: str) -> Applicant:
        cache_key = f"token:{token}:applicant"
        applicant = cache.get(cache_key)
        if applicant is not None:
            if applicant.quitted:
                raise PermissionDenied({"detail": "Applicant has quitted"})
            return applicant

        token_obj = Token.objects.filter(token=token).first()
        if token_obj is None:
            raise AuthenticationFailed({"detail": "Token is invalid"})
        # Check if applicant exists for this wechat_info
        wechat_info = token_obj.wechat_info
        try:
            applicant = Applicant.objects.get(wechat_info=wechat_info)
            if applicant.quitted:
                raise PermissionDenied({"detail": "Applicant has quitted"})
            cache.set(cache_key, applicant, timeout=3600)  # Cache for 1 hour
            return applicant
        except Applicant.DoesNotExist:
            raise NotFound({"detail": "Applicant not found"})

    def get_applicant_by_openid(self, openid: str) -> Applicant:
        cache_key = f"applicant:openid:{openid}"
        applicant = cache.get(cache_key)
        if applicant is not None:
            return applicant

        try:
            applicant = Applicant.objects.get(wechat_info__openid=openid)
            cache.set(cache_key, applicant, timeout=3600)  # Cache for 1 hour
            return applicant
        except Applicant.DoesNotExist:
            raise NotFound({"detail": "Applicant not found"})

    def get_match_by_applicant(self, applicant: Applicant) -> tuple[Match, int]:
        cache_key = f"match:applicant:{applicant.id}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        try:
            match = (
                Match.objects.filter(Q(applicant1=applicant) | Q(applicant2=applicant))
                .order_by("-id")
                .first()
            )
            if match is None:
                raise NotFound({"detail": "Match not found"})
            if match.applicant1 == applicant:
                result = (match, 1)
            else:
                result = (match, 2)
            cache.set(cache_key, result, timeout=3600)  # Cache for 1 hour
            return result
        except Match.DoesNotExist:
            raise NotFound({"detail": "Match not found"})

    def get_task_by_match_and_day(self, match: Match, day: int) -> Task:
        cache_key = f"task:match:{match.id}:day:{day}"
        task = cache.get(cache_key)
        if task is not None:
            return task

        try:
            task = Task.objects.get(match=match, day=day)
            cache.set(cache_key, task, timeout=3600)  # Cache for 1 hour
            return task
        except Task.DoesNotExist:
            task = Task.objects.create(match=match, day=day)
            cache.set(cache_key, task, timeout=3600)  # Cache for 1 hour
            return task

    def get_mission_by_day(self, day: int) -> Mission | None:
        cache_key = f"mission:day:{day}"
        mission = cache.get(cache_key)
        if mission is not None:
            return mission

        mission = Mission.objects.filter(day=day).first()
        # Cache even if missing to reduce repeated DB hits
        cache.set(cache_key, mission, timeout=3600)  # Cache for 1 hour
        return mission

    def assert_match_not_discarded(self, match: Match):
        if match.discarded:
            raise PermissionDenied({"detail": "Match has been discarded"})

    def assert_day_valid(self, day: int):
        if not (1 <= day <= 7):
            raise ValidationError({"detail": "Day must be between 1 and 7"})

    def calculate_rank(self) -> dict[int, dict]:
        """
        Calculate ranks for all non-discarded matches. Returns a dict mapping match_id
        to {"rank": int, "total_score": int, "group_name": str}. Cached for 15 minutes.
        """
        cache_key = "match:ranking:all"
        # Get all matches with their total scores and group names
        matches = (
            Match.objects.filter(discarded=False)
            .annotate(
                score=Sum(
                    F("tasks__basic_score")
                    + F("tasks__bonus_score")
                    + F("tasks__daily_score")
                    + F("tasks__uni_score")
                )
            )
            .order_by("-score", "id")
        )  # Order by score descending, then by id for consistency

        # Build list of (match_id, score, group_name) tuples
        match_scores = [
            (match.id, match.score or 0, match.name or "未知")
            for match in matches
        ]

        # Calculate ranks with proper tie handling; store rank, total_score, group_name
        ranking_dict = {}
        current_rank = 1
        i = 0

        while i < len(match_scores):
            match_id_at_i, score, group_name = match_scores[i]
            # Count how many matches have the same score
            tied_count = 1
            j = i + 1
            while j < len(match_scores) and match_scores[j][1] == score:
                tied_count += 1
                j += 1

            # Assign the same rank to all tied matches; store rank, total_score, group_name
            for k in range(i, i + tied_count):
                mid, total_score, name = match_scores[k]
                ranking_dict[mid] = {
                    "rank": current_rank,
                    "total_score": int(total_score),
                    "group_name": name,
                }

            # Same score = one place: next distinct score gets current_rank + 1 (dense ranking)
            current_rank += 1
            i += tied_count

        # Cache the ranking dictionary for 15 minutes
        cache.set(cache_key, ranking_dict, timeout=900)  # 15 minutes = 900 seconds
        return ranking_dict

    def get_all_ranks(self) -> dict[int, dict]:
        """Returns dict mapping match_id to {'rank', 'total_score', 'group_name'}."""
        cache_key = "match:ranking:all"
        ranking_dict = cache.get(cache_key)
        if ranking_dict is not None:
            return ranking_dict
        ranking_dict = self.calculate_rank()
        cache.set(cache_key, ranking_dict, timeout=900)  # 15 minutes = 900 seconds
        return ranking_dict

    def get_current_day(self) -> int:
        """Get current day (1–7) based on FIRST_MISSION_RELEASE."""
        day = (configs.AvtivityDates.now() - configs.AvtivityDates.FIRST_MISSION_END).days + 2
        return max(min(day, 7), 1)

    def calculate_daily_rank(self, day: int) -> dict[int, dict]:
        """
        Calculate ranks for a specific day's score. Returns dict mapping match_id
        to {"rank": int, "total_score": int, "group_name": str}. Same structure as
        calculate_rank() but scores are from tasks for that day only.
        """
        cache_key = f"match:ranking:daily"
        ranking_dict = cache.get(cache_key)
        if ranking_dict is not None:
            return ranking_dict

        day_score_expr = Case(
            When(tasks__day=day, then=(
                F("tasks__basic_score")
                + F("tasks__bonus_score")
                + F("tasks__daily_score")
                + F("tasks__uni_score")
            )),
            default=Value(0),
            output_field=IntegerField(),
        )
        matches = (
            Match.objects.filter(discarded=False)
            .annotate(score=Sum(day_score_expr))
            .order_by("-score", "id")
        )

        match_scores = [
            (match.id, match.score or 0, match.name or "未知")
            for match in matches
        ]

        ranking_dict = {}
        current_rank = 1
        i = 0

        while i < len(match_scores):
            score = match_scores[i][1]
            tied_count = 1
            j = i + 1
            while j < len(match_scores) and match_scores[j][1] == score:
                tied_count += 1
                j += 1

            for k in range(i, i + tied_count):
                mid, total_score, name = match_scores[k]
                ranking_dict[mid] = {
                    "rank": current_rank,
                    "total_score": int(total_score),
                    "group_name": name,
                }

            current_rank += 1
            i += tied_count

        cache.set(cache_key, ranking_dict, timeout=900)
        return ranking_dict

    def get_daily_ranks(self, day: int) -> dict[int, dict]:
        """Returns dict mapping match_id to {'rank', 'total_score', 'group_name'} for given day."""
        return self.calculate_daily_rank(day)

    def get_rank(self, match_id: int) -> int:
        """
        Get the rank of a match. Calculates ranks for all matches and caches them for 15 minutes.
        Handles ties properly: matches with the same score get the same rank.

        Args:
            match_id: The ID of the match to get the rank for

        Returns:
            The rank of the match (1 is highest score), or -1 if not in ranking
        """
        cache_key = "match:ranking:all"
        ranking_dict = cache.get(cache_key)

        if ranking_dict is None:
            ranking_dict = self.calculate_rank()

        entry = ranking_dict.get(match_id)
        return entry["rank"] if entry else -1

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
from django.db.models import Q, Sum, F

from . import configs
from .models import Applicant, Token, Match, WeChatInfo, Task


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

    def assert_match_not_discarded(self, match: Match):
        if match.discarded:
            raise PermissionDenied({"detail": "Match has been discarded"})

    def assert_day_valid(self, day: int):
        if not (1 <= day <= 7):
            raise ValidationError({"detail": "Day must be between 1 and 7"})

    def get_rank(self, match_id: int) -> int:
        """
        Get the rank of a match. Calculates ranks for all matches and caches them for 15 minutes.
        Handles ties properly: matches with the same score get the same rank.

        Args:
            match_id: The ID of the match to get the rank for

        Returns:
            The rank of the match (1 is highest score)
        """
        cache_key = "match:ranking:all"
        ranking_dict = cache.get(cache_key)

        if ranking_dict is None:
            # Calculate ranks for all matches
            # Get all matches with their total scores
            matches = Match.objects.annotate(
                score=Sum(
                    F("tasks__basic_score")
                    + F("tasks__bonus_score")
                    + F("tasks__daily_score")
                )
            ).order_by(
                "-score", "id"
            )  # Order by score descending, then by id for consistency

            # Build list of (match_id, score) tuples
            match_scores = [(match.id, match.score or 0) for match in matches]

            # Calculate ranks with proper tie handling
            ranking_dict = {}
            current_rank = 1
            i = 0

            while i < len(match_scores):
                match_id_at_i, score = match_scores[i]
                # Count how many matches have the same score
                tied_count = 1
                j = i + 1
                while j < len(match_scores) and match_scores[j][1] == score:
                    tied_count += 1
                    j += 1

                # Assign the same rank to all tied matches
                for k in range(i, i + tied_count):
                    ranking_dict[match_scores[k][0]] = current_rank

                # Move to next rank (skip tied positions)
                current_rank += tied_count
                i += tied_count

            # Cache the ranking dictionary for 15 minutes
            cache.set(cache_key, ranking_dict, timeout=900)  # 15 minutes = 900 seconds

        # Return the rank for the requested match
        # If match not found in ranking (shouldn't happen normally), return None
        return ranking_dict.get(match_id)

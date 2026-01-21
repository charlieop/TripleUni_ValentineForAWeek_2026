from datetime import timedelta
from rest_framework.exceptions import (
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
from django.db.models import Q

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


class UtilMixin:
    def get_token(self, request: Request) -> str:
        token = request.headers.get("Authorization")
        if token is None:
            raise ParseError('Authorization header with user "token" is required')
        return token

    def get_openid_by_token(self, token: str) -> str:
        token_obj = Token.objects.filter(token=token).first()
        if token_obj is None:
            raise ParseError("Token is invalid")
        openid = token_obj.wechat_info.openid
        return openid

    def get_wechat_info_by_token(self, token: str) -> WeChatInfo:
        token_obj = Token.objects.filter(token=token).first()
        if token_obj is None:
            raise ParseError("Token is invalid")
        return token_obj.wechat_info

    def get_applicant_by_token(self, token: str) -> Applicant:
        token_obj = Token.objects.filter(token=token).first()
        if token_obj is None:
            raise ParseError("Token is invalid")
        # Check if applicant exists for this wechat_info
        wechat_info = token_obj.wechat_info
        try:
            applicant = Applicant.objects.get(wechat_info=wechat_info)
            if applicant.quitted:
                raise PermissionDenied("Applicant has quitted")
            return applicant
        except Applicant.DoesNotExist:
            raise NotFound("Applicant not found")
        
    def get_match_by_applicant(self, applicant: Applicant) -> tuple[Match, int]:
        try:
            match = Match.objects.filter(Q(applicant1=applicant) | Q(applicant2=applicant)).order_by("-id").first()
            if match is None:
                raise NotFound("Match not found")
            if match.applicant1 == applicant:
                return match, 1
            else:
                return match, 2
        except Match.DoesNotExist:
            raise NotFound("Match not found")
        
    def get_task_by_match_and_day(self, match: Match, day: int) -> Task:
        try:
            task =  Task.objects.get(match=match, day=day)
        except Task.DoesNotExist:
            task  = Task.objects.create(match=match, day=day)
        return task
        
    def assert_match_not_discarded(self, match: Match):
        if match.discarded:
            raise PermissionDenied("Match has been discarded")
        
    def assert_day_valid(self, day: int):
        if not (1 <= day <= 7):
            raise ValidationError("Day must be between 1 and 7")


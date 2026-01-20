from datetime import timedelta
from rest_framework.exceptions import (
    APIException,
    ParseError,
    NotFound,
)
import uuid
import pickle
from django.core.cache import cache
from django.db.models import Q

from .models import Applicant, Token


class Gone(APIException):
    status_code = 410
    default_detail = "The requested resource is no longer available."
    default_code = "gone"


class Conflict(APIException):
    status_code = 409
    default_detail = "A conflict occurred."
    default_code = "conflict"


class UtilMixin:
    def get_token(self, request):
        token = request.headers.get("Authorization")
        if token is None:
            raise ParseError('Authorization header with user "token" is required')
        return token

    def get_openid_by_token(self, token):
        token_obj = Token.objects.filter(token=token).first()
        if token_obj is None:
            raise ParseError("Token is invalid")
        openid = token_obj.wechat_info.openid
        return openid

    def get_wechat_info_by_token(self, token):
        token_obj = Token.objects.filter(token=token).first()
        if token_obj is None:
            raise ParseError("Token is invalid")
        return token_obj.wechat_info

    def get_applicant_by_token(self, token):
        token_obj = Token.objects.filter(token=token).first()
        if token_obj is None:
            raise ParseError("Token is invalid")
        # Check if applicant exists for this wechat_info
        wechat_info = token_obj.wechat_info
        try:
            applicant = Applicant.objects.get(wechat_info=wechat_info)
            if applicant.quitted:
                raise Gone("Applicant has quitted")
            return applicant
        except Applicant.DoesNotExist:
            raise NotFound("Applicant not found")

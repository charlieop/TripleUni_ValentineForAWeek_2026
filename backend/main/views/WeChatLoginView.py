import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.base import ContentFile

from django.conf import settings
import json

from ..models import WeChatInfo, Token
from ..logger import CustomLogger

logger = CustomLogger("wechat_login")

with open(settings.BASE_DIR / "SECRETS.json") as f:
    secrets = json.load(f)
    APP_ID = secrets["WECHAT_APP_ID"]
    SECRET = secrets["WECHAT_APP_SECRET"]


@api_view(["POST"])
def wechat_oauth_view(request):
    logger.newline()
    logger.info("POST /login - WeChat OAuth login attempt")

    if "code" not in request.data:
        logger.error("Login failed: code not found")
        return Response("code not found", status=status.HTTP_400_BAD_REQUEST)

    code = request.data["code"]

    # fetch access token
    ACCESS_TOKEN_URL = (
        "https://api.weixin.qq.com/sns/oauth2/access_token?"
        f"appid={APP_ID}&"
        f"secret={SECRET}&"
        f"code={code}&"
        "grant_type=authorization_code"
    )

    response = requests.get(ACCESS_TOKEN_URL)
    if response.status_code != 200:
        logger.error("Failed to get Access Token from WeChat API")
        return Response(
            "Failed to get Access Token", status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    content = response.json()
    if "errcode" in content:
        logger.error(f"WeChat API error: {content['errmsg']}")
        return Response(
            {"detail": content["errmsg"]}, status=status.HTTP_400_BAD_REQUEST
        )

    ACCESS_TOKEN = content["access_token"]
    OPENID = content["openid"]
    UNIONID = content["unionid"]

    logger.info(f"Got access token for openid: {OPENID}")

    # fetch user info
    USER_INFO_URL = (
        f"https://api.weixin.qq.com/sns/userinfo?"
        f"access_token={ACCESS_TOKEN}&"
        f"openid={OPENID}&"
        f"lang=zh_CN"
    )

    user_info_response = requests.get(USER_INFO_URL)
    if user_info_response.status_code != 200:
        logger.error(f"Failed to get user info for openid: {OPENID}")
        return Response(
            {"detail": "failed to get user info"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    user_info_content = user_info_response.json()
    if "errcode" in user_info_content:
        logger.error(
            f"WeChat userinfo API error for openid {OPENID}: {user_info_content['errmsg']}"
        )
        return Response(
            {"detail": user_info_content["errmsg"]}, status=status.HTTP_400_BAD_REQUEST
        )

    NICKNAME = user_info_content["nickname"].encode("iso-8859-1").decode("utf-8")
    HEADIMGURL = user_info_content["headimgurl"].encode("iso-8859-1").decode("utf-8")
    HEADIMGURL = HEADIMGURL.rsplit("/", 1)[0] + "/0"

    logger.info(f"Fetched user info for openid: {OPENID}, nickname: {NICKNAME}")

    return _saveToModel(OPENID, NICKNAME, HEADIMGURL, UNIONID)


def _saveToModel(openid, nickname, headimgurl, unionid):
    existing_user = WeChatInfo.objects.filter(openid=openid).first()
    if existing_user:
        logger.info(f"Existing user login: {openid}")
        existing_user.nickname = nickname
        if existing_user.head_image_url != headimgurl:
            image_file = _fetchImage(openid, headimgurl)
            if image_file:
                existing_user.head_image = image_file
                existing_user.head_image_url = headimgurl
                logger.info(f"Updated head image for: {openid}")
        existing_user.save()

        try:
            token = existing_user.token
        except Token.DoesNotExist:
            token = Token.objects.create(wechat_info=existing_user)
        logger.info(f"Login successful for: {openid}")
        return Response({"data": {"token": token.token}}, status=status.HTTP_200_OK)

    # If the user does not exist, proceed to create a new one
    logger.info(f"New user registration: {openid}")
    image_file = _fetchImage(openid, headimgurl)
    if not image_file:
        logger.error(f"Failed to fetch head image for new user: {openid}")
        return Response(
            {"detail": "Failed to fetch image"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    data = {
        "openid": openid,
        "unionid": unionid,
        "nickname": nickname,
        "head_image": image_file,
        "head_image_url": headimgurl,
    }
    newWeChatInfo = WeChatInfo(**data)

    try:
        newWeChatInfo.full_clean()
        newWeChatInfo.save()
        logger.info(f"Created new WeChatInfo for: {openid}")
    except Exception as e:
        logger.error(f"Failed to save new WeChatInfo for {openid}: {str(e)}")
        return Response(
            {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    token = Token.objects.create(wechat_info=newWeChatInfo)
    if not token:
        logger.error(f"Failed to create token for new user: {openid}")
        return Response(
            {"detail": "Failed to create token"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    logger.info(f"Registration successful for: {openid}")
    return Response({"data": {"token": token.token}}, status=status.HTTP_200_OK)


def _fetchImage(openid, url):
    image_response = requests.get(url)
    if image_response.status_code != 200:
        return None
    image_file = ContentFile(image_response.content)
    image_file.name = f"{openid}.jpg"
    return image_file

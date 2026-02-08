import requests
from celery import shared_task
from django.core.files.base import ContentFile
from django.db import transaction

from .logger import CustomLogger
from .models import WeChatInfo
from .mixin import UtilMixin

MAX_RETRIES = 3
TIMEOUT = 15
logger = CustomLogger("wechat_avatar")
logger_calculate_match_ranks = CustomLogger("calculate_match_ranks")

@shared_task
def update_wechat_avatar(openid: str, headimgurl: str) -> None:
    """
    Download the latest WeChat avatar and update the corresponding WeChatInfo.

    This task is intentionally fire-and-forget: failures are logged but do not
    affect the login flow with a retry mechanism.
    """
    logger.newline()
    logger.info(f"[Celery] Updating avatar for openid={openid}, headimgurl={headimgurl}")

    for i in range(MAX_RETRIES):
        try:
            image_response = requests.get(headimgurl, timeout=TIMEOUT)
        except Exception as e:
            logger.error(f"[Celery] Failed to fetch image for {openid}: {e} (attempt {i+1})")
            continue
        break

    if image_response.status_code != 200:
        logger.error(
            f"[Celery] Non-200 response when fetching image for {openid}: "
            f"{image_response.status_code}"
        )
        return

    image_file = ContentFile(image_response.content)
    image_file.name = "temp.jpg"

    try:
        with transaction.atomic():
            user = WeChatInfo.objects.select_for_update().get(openid=openid)
            user.head_image = image_file
            user.head_image_url = headimgurl
            user.save()
            logger.info(f"[Celery] Successfully updated avatar for {openid}")
    except WeChatInfo.DoesNotExist:
        logger.error(
            f"[Celery] WeChatInfo does not exist for openid={openid} while updating avatar"
        )
    except Exception as e:
        logger.error(
            f"[Celery] Unexpected error while updating avatar for {openid}: {e}"
        )


@shared_task
def calculate_match_ranks() -> None:
    """
    Periodic task to calculate and cache ranking for all matches.

    This calls UtilMixin.calculate_rank(), which writes the ranking dict into
    the cache under the key 'match:ranking:all'.
    """
    util = UtilMixin()
    util.calculate_rank()
    logger_calculate_match_ranks.info("[Celery] Successfully calculated match ranks")
import requests
from celery import shared_task
from django.core.files.base import ContentFile
from django.db import transaction

from .logger import CustomLogger
from .models import Task, WeChatInfo
from .mixin import UtilMixin

MAX_RETRIES = 3
TIMEOUT = 15
logger = CustomLogger("wechat_avatar")
logger_calculate_match_ranks = CustomLogger("calculate_match_ranks")
logger_grade_batch = CustomLogger("grade_batch")

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
    util.calculate_daily_rank(util.get_current_day())
    logger_calculate_match_ranks.info("[Celery] Successfully calculated match ranks")


def _grade_day_batch(day: int) -> None:
    """Filter tasks for the given day and call Autograder.grade_batch."""
    from .autograder.autograder import Autograder

    tasks = list(
        Task.objects.filter(day=day).select_related("match").order_by("match_id")
    )
    logger_grade_batch.info(f"[Celery] Grading day {day} batch: {len(tasks)} tasks")
    if not tasks:
        logger_grade_batch.info(f"[Celery] No tasks for day {day}, skipping")
        return
    autograder = Autograder(day=day)
    autograder.grade_batch(tasks)
    logger_grade_batch.info(f"[Celery] Successfully graded day {day} batch")


@shared_task
def grade_day1_batch() -> None:
    """Grade all tasks belonging to day 1."""
    _grade_day_batch(1)


@shared_task
def grade_day2_batch() -> None:
    """Grade all tasks belonging to day 2."""
    _grade_day_batch(2)


@shared_task
def grade_day3_batch() -> None:
    """Grade all tasks belonging to day 3."""
    _grade_day_batch(3)


@shared_task
def grade_day4_batch() -> None:
    """Grade all tasks belonging to day 4."""
    _grade_day_batch(4)


@shared_task
def grade_day5_batch() -> None:
    """Grade all tasks belonging to day 5."""
    _grade_day_batch(5)


@shared_task
def grade_day6_batch() -> None:
    """Grade all tasks belonging to day 6."""
    _grade_day_batch(6)


@shared_task
def grade_day7_batch() -> None:
    """Grade all tasks belonging to day 7."""
    _grade_day_batch(7)


@shared_task
def grade_batch_for_task_ids(day: int, task_ids: list[int]) -> None:
    """
    Grade the given tasks (must all be for the same day).
    Used by admin "批改选中任务" action to run grading asynchronously.
    """
    from .autograder.autograder import Autograder

    tasks = list(
        Task.objects.filter(pk__in=task_ids)
        .select_related("match")
        .order_by("match_id")
    )
    if not tasks:
        logger_grade_batch.info(
            f"[Celery] No tasks for day {day} (ids={task_ids}), skipping"
        )
        return
    logger_grade_batch.info(
        f"[Celery] Grading day {day} batch: {len(tasks)} tasks (selected)"
    )
    autograder = Autograder(day=day)
    autograder.grade_batch(tasks)
    logger_grade_batch.info(f"[Celery] Successfully graded day {day} batch")
import requests
import json

from .models import Applicant, Match
from django.db.models import Q
from .logger import CustomLogger
from .configs import AvtivityDates

from django.conf import settings
with open(settings.BASE_DIR / "SECRETS.json") as f:
    secrets = json.load(f)
    APP_ID = secrets["WECHAT_APP_ID"]
    SECRET = secrets["WECHAT_APP_SECRET"]
    
ACCESS_TOKEN_URL = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={SECRET}"
TEMPLATE_ID = "7I5ojpzz5V6Vrz4Xk445zZQdJK42SkFD-PrRS-WTiJg"
JUMP_URL = "https://valentine.tripleuni.com"

logger = CustomLogger("utils")

class AccessTokenExpired(Exception):
    pass


def get_push_message_url(access_token: str) -> str:
    return f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"

def get_access_token() -> str:
    response = requests.get(ACCESS_TOKEN_URL)
    if response.status_code != 200:
        logger.critical(f"Failed to get access token: {response.status_code}")
        raise Exception(f"Failed to get access token: {response.status_code}")
    data = response.json()
    if "access_token" not in data:
        logger.critical(f"Failed to get access token: {data}")
        raise Exception(f"Failed to get access token: {data}")
    return data["access_token"]


def send_notification_to_user(push_message_url: str, openid: str, title: str, date: str, content: str, jump_path: str = None, msg_id: str = None) -> bool:
    payload = {
        "touser": openid,
        "template_id": TEMPLATE_ID,
        "data": {
            "keyword1": {"value": title},
            "keyword2": {"value": date},
            "keyword3": {"value": content},
        },
        "url": f"{JUMP_URL}/{jump_path}",
        "client_msg_id": msg_id,
    }
    response = requests.post(push_message_url, json=payload)
    if response.status_code != 200:
        logger.critical(f"Failed to send notification to user {openid}: {response.status_code}, aborting...")
        raise Exception(f"Failed to send notification to user {openid}: {response.status_code}")
    
    data = response.json()
    errcode = data.get("errcode", None)
    if errcode == 40001:
        logger.error(f"Access token expired, retuire refreshing...")
        raise AccessTokenExpired()
    elif errcode == 43004:
        logger.warning(f"User {openid} is not subscribed, skipping...")
        return False
    elif errcode == -1:
        logger.critical(f"Wechat API error: {data}")
        raise Exception(f"Wechat API error: {data}")
    elif errcode != 0:
        logger.error(f"Failed to send notification to user {openid}: {data}")
        return False
    logger.info(f"Successfully sent notification to user {openid}, msg_id: {data.get('msgid', None)}")
    return True


def send_notification_to_users(openids: list[str], title: str, date: str, content: str, jump_path: str = None, msg_id: str = None) -> bool:
    logger.newline()
    logger.info(f"Sending notification to {len(openids)} users: {title} {date} {content} with msg_id: {msg_id}")
    
    access_token = get_access_token()
    push_message_url = get_push_message_url(access_token)
    
    processing_idx = 0
    total_openids = len(openids)
    
    while processing_idx < total_openids:
        try:
            openid = openids[processing_idx]
            send_notification_to_user(push_message_url, openid, title, date, content, jump_path, msg_id)
            processing_idx += 1
        except AccessTokenExpired:
            access_token = get_access_token()
            push_message_url = get_push_message_url(access_token)
        except Exception as e:
            logger.critical(f"Message sent failed at {processing_idx}/{total_openids}")
            logger.newline()
            processing_idx += 1
            return False
    logger.info(f"Successfully sent notification to {processing_idx} users")
    return True


def remind_payment_to_not_paid_applicants() -> bool:
    applicants = Applicant.objects.filter(Q(payment__isnull=True) & Q(quitted=False))
    openids = [applicant.wechat_info.openid for applicant in applicants]
    
    if len(openids) == 0:
        logger.info("No applicants to remind to pay押金")
        return True
    
    logger.info(f"Reminding {len(openids)} applicants to pay deposit")

    title = "一周CP 2026 押金支付提醒"
    date = AvtivityDates.now().strftime("%Y-%m-%d")
    content = "活动报名即将截止，请尽快支付押金，否则将无法参加活动"
    jump_path = "payment"
    msg_id = "payment_reminder"

    success =  send_notification_to_users(openids, title, date, content, jump_path, msg_id)
    logger.info(f"Finished sending notification to {len(openids)} applicants: {success}")
    return success

def notify_first_match_result_to_all() -> bool:
    applicants = Applicant.objects.filter(Q(payment__isnull=False) & Q(quitted=False))
    openids = [applicant.wechat_info.openid for applicant in applicants]
    
    if len(openids) == 0:
        logger.info("No applicants to notify first match result")
        return True
    
    logger.info(f"Notifying {len(openids)} applicants first match result")
    
    title = "一周CP 2026 第一轮匹配结果"
    date = AvtivityDates.now().strftime("%Y-%m-%d")
    content = "第一轮匹配结果已发布，请登录网站查看"
    jump_path = "match-result"
    msg_id = "first_match_result_notification"
    
    success = send_notification_to_users(openids, title, date, content, jump_path, msg_id)
    
    logger.info(f"Finished sending notification to {len(openids)} applicants: {success}")
    return success

def notify_first_match_result_to_not_confirmed_applicants() -> bool:
    # all the applicants that is in a match and is still having state P:
    first_round_matches = Match.objects.filter(Q(round=1) & Q(discarded=False))
    pending_matches = first_round_matches.filter(Q(applicant1_status="P") | Q(applicant2_status="P"))
    pending_applicants = [match.applicant1 for match in pending_matches if match.applicant1_status == "P"] + [match.applicant2 for match in pending_matches if match.applicant2_status == "P"]
    openids = [applicant.wechat_info.openid for applicant in pending_applicants]
    
    if len(openids) == 0:
        logger.info("No applicants to notify first match result confirm reminder")
        return True
    
    logger.info(f"Notifying {len(openids)} applicants first match result confirm reminder")
    
    title = "一周CP 2026 第一轮确认即将截止"
    date = AvtivityDates.now().strftime("%Y-%m-%d")
    content = "第一轮确认即将截止，请尽快确认匹配结果，否则本次匹配将失效"
    jump_path = "match-result"
    msg_id = "first_match_result_confirm_reminder"
    
    success = send_notification_to_users(openids, title, date, content, jump_path, msg_id)
    logger.info(f"Finished sending notification to {len(openids)} applicants: {success}")
    return success

def notify_second_match_result_to_all() -> bool:
    second_round_matches = Match.objects.filter(Q(round=2) & Q(discarded=False))
    applicants = [match.applicant1 for match in second_round_matches] + [match.applicant2 for match in second_round_matches]
    openids = [applicant.wechat_info.openid for applicant in applicants]
    
    if len(openids) == 0:
        logger.info("No applicants to notify second match result")
        return True
    
    logger.info(f"Notifying {len(openids)} applicants second match result")
    
    title = "一周CP 2026 第二轮匹配结果"
    date = AvtivityDates.now().strftime("%Y-%m-%d")
    content = "第二轮匹配结果已发布，请登录网站查看"
    jump_path = "match-result"
    msg_id = "second_match_result_notification"
    
    success = send_notification_to_users(openids, title, date, content, jump_path, msg_id)
    logger.info(f"Finished sending notification to {len(openids)} applicants: {success}")
    return success

def notify_activity_start_to_all() -> bool:
    valid_matches = Match.objects.filter(discarded=False)
    applicants = [match.applicant1 for match in valid_matches] + [match.applicant2 for match in valid_matches]
    openids = [applicant.wechat_info.openid for applicant in applicants]
    
    if len(openids) == 0:
        logger.info("No applicants to notify activity start")
        return True
    
    logger.info(f"Notifying {len(openids)} applicants activity start")
    
    title = "一周CP 2026 活动即将开始"
    date = AvtivityDates.now().strftime("%Y-%m-%d")
    content = "活动即将开始，祝你们度过美好的一周！"
    jump_path = "match"
    msg_id = "activity_start_reminder"
    
    success = send_notification_to_users(openids, title, date, content, jump_path, msg_id)
    logger.info(f"Finished sending notification to {len(openids)} applicants: {success}")
    return success

def notify_daily_task_deadline_to_all(day: int) -> bool:
    valid_matches = Match.objects.filter(discarded=False)
    applicants = [match.applicant1 for match in valid_matches] + [match.applicant2 for match in valid_matches]
    openids = [applicant.wechat_info.openid for applicant in applicants]
    
    if len(openids) == 0:
        logger.info("No applicants to notify daily task deadline")
        return True
    
    logger.info(f"Notifying {len(openids)} applicants daily task deadline")
    
    title = f"一周CP 2026 第{day}天任务提交截止提醒"
    date = AvtivityDates.now().strftime("%Y-%m-%d")
    content = f"第{day}天任务提交快要截止啦! 别忘了提交任务哦~"
    jump_path = "match"
    msg_id = f"daily_task_deadline_reminder_{day}"
    
    success = send_notification_to_users(openids, title, date, content, jump_path, msg_id)
    logger.info(f"Finished sending notification to {len(openids)} applicants: {success}")
    return success

def notify_exit_questionnaire_deadline_to_all() -> bool:
    valid_matches = Match.objects.filter(discarded=False)
    applicants = [match.applicant1 for match in valid_matches] + [match.applicant2 for match in valid_matches]
    openids = [applicant.wechat_info.openid for applicant in applicants]
    
    if len(openids) == 0:
        logger.info("No applicants to notify exit questionnaire deadline")
        return True
    
    logger.info(f"Notifying {len(openids)} applicants exit questionnaire deadline")
    
    title = "一周CP 2026 结束问卷提交截止提醒"
    date = AvtivityDates.now().strftime("%Y-%m-%d")
    content = "结束问卷提交快要截止啦! 别忘了提交问卷哦~"
    jump_path = "exit-questionnaire"
    msg_id = "exit_questionnaire_deadline_reminder"
    
    success = send_notification_to_users(openids, title, date, content, jump_path, msg_id)
    logger.info(f"Finished sending notification to {len(openids)} applicants: {success}")
    return success
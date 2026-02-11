import base64
from itertools import islice
import json
import requests

from django.conf import settings

from ..models import Mission, Task
from ..logger import CustomLogger

API_URL = "https://eo.api.tripleuuunnniii.com/v4/valentine/getusercontent.php"

with open(settings.BASE_DIR / "SECRETS.json") as f:
    secrets = json.load(f)
    UNI_APPID = secrets["UNI_APPID"]
    UNI_APPKEY = secrets["UNI_APPKEY"]

logger = CustomLogger("autograder_utils")

def batched(iterator, batch_size):
    it = iter(iterator)
    while True:
        batch = list(islice(it, batch_size))
        if not batch:
            return
        yield batch

def get_mission_prompt(day: int) -> str:
    mission = Mission.objects.get(day=day)
    return mission.prompt

def get_all_base64_images(task: Task):
    image_paths = [img.image.path for img in task.imgs.filter(deleted = False).order_by("created_at")]
    return [
        base64.b64encode(open(image_path, "rb").read()).decode("utf-8")
        for image_path in image_paths
    ]
    
def save_response_to_tasks(day: int, response: dict, use_thinking: bool):
    for match_id, text in response.items():
        task = Task.objects.get(match_id=match_id, day=day)
        
        try:
            if use_thinking:
                thinking_process, score_json = text.split("</think>")
            else:
                thinking_process, score_json = "未使用思考过程", text
            score = json.loads(score_json)
        except Exception as e:
            logger.error(f"Error while saving response to tasks for task {task}: {e}")
            score = {
                "basic": {
                    "score": 0,
                    "reason": "模型评分失败, 请联系你的Mentor"
                },
                "bonus": {
                    "score": 0,
                    "reason": "模型评分失败, 请联系你的Mentor"
                },
                "daily": {
                    "score": 0,
                    "reason": "模型评分失败, 请联系你的Mentor"
                },
                "basic_completed": False,
                "completed_offline_task": False,
                "offline_task": {
                    "score": 0,
                    "reason": "模型评分失败, 请联系你的Mentor"
                }
            }
            thinking_process = text
        
        task.basic_completed = score.get("basic_completed", False)
        task.basic_score = score.get("basic", {}).get("score", 0)
        task.bonus_score = score.get("bonus", {}).get("score", 0)
        task.daily_score = score.get("daily", {}).get("score", 0)
        
        task.basic_review = score.get("basic", {}).get("reason", "")
        task.bonus_review = score.get("bonus", {}).get("reason", "")
        task.daily_review = score.get("daily", {}).get("reason", "")

        task.thinking_process = thinking_process
        
        if day >= 5 and score.get("completed_offline_task", False):
            match = task.match
            if not match.completed_offline_task:
                match.completed_offline_task = True
                match.save()
                logger.info(f"Task {task} Match {match} completed offline task")
                task.basic_score += score.get("offline_task", {}).get("score", 0)
                task.basic_review = str(task.basic_review) + "\n" + score.get("offline_task", {}).get("reason", "")
            else:
                logger.info(f"Task {task} Match {match} already completed offline task")
                task.basic_review = str(task.basic_review) + "\n" + "之前已经完成过线下任务, 不再重复加分"
        task.save()
        
def remove_empty_payload(payload: dict, day: int) -> dict:
    empty_payload = {mid: data for mid, data in payload.items() if len(data["base64_images"]) == 0}
    for mid in empty_payload.keys():
        task = Task.objects.get(match_id=mid, day=day)
        task.basic_completed = False
        task.basic_score = 0
        task.bonus_score = 0
        task.daily_score = 0
        task.basic_review = "未上传图片, 提交内容为空"
        task.bonus_review = "未上传图片, 提交内容为空"
        task.daily_review = "未上传图片, 提交内容为空"
        task.thinking_process = "未上传图片, 提交内容为空"
        task.save()
        del payload[mid]
    return payload
        

def get_tripleuni_post_record(task: Task, start_time_unix: int, end_time_unix: int) -> bool:
    match = task.match
    applicant1 = match.applicant1
    applicant2 = match.applicant2
    
    if applicant1.linked_uni:
        applicant1_email = applicant1.email
        uni_task_completed = _query_tripleuni_post_record(applicant1_email, start_time_unix, end_time_unix)
        if uni_task_completed:
            return True
        
    if applicant2.linked_uni:
        applicant2_email = applicant2.email
        uni_task_completed = _query_tripleuni_post_record(applicant2_email, start_time_unix, end_time_unix)
        if uni_task_completed:
            return True
            
    return False

def _query_tripleuni_post_record(email: str, start_time_unix: int, end_time_unix: int) -> bool:
    payload = f"appid={UNI_APPID}&appkey={UNI_APPKEY}&user_email={email}&start_time={start_time_unix}&end_time={end_time_unix}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request("POST", API_URL, data=payload, headers=headers)
    data = response.json()
    if "post_list" in data:
        return len(data["post_list"]) > 0
    else:
        return False
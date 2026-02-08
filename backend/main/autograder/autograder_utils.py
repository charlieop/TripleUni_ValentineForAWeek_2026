import base64
from itertools import islice
import json

from ..models import Mission, Task


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
        if use_thinking:
            thinking_process, score_json = text.split("</think>")
        else:
            thinking_process, score_json = "未使用思考过程", text
        
        score = json.loads(score_json)
        task.basic_completed = score.get("basic_completed", False)
        task.basic_score = score.get("basic", {}).get("score", 0)
        task.bonus_score = score.get("bonus", {}).get("score", 0)
        task.daily_score = score.get("daily", {}).get("score", 0)
        
        task.basic_review = score.get("basic", {}).get("reason", "")
        task.bonus_review = score.get("bonus", {}).get("reason", "")
        task.daily_review = score.get("daily", {}).get("reason", "")

        task.thinking_process = thinking_process

        task.scored = True
        task.save()
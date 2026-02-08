import modal

from ..models import Match, Task
from ..logger import CustomLogger

from .autograder_utils import batched, get_mission_prompt, get_all_base64_images, save_response_to_tasks

logger = CustomLogger("autograder")

class Autograder():
    def __init__(self, day: int, batch_size: int = 10, use_thinking: bool = True):
        self.day = day
        self.batch_size = batch_size
        self.use_thinking = use_thinking
        if self.use_thinking:
            self.Qwen3VL = modal.Cls.from_name("qwen3-vl-thinking", "Qwen3VLThinking")
        else:
            self.Qwen3VL = modal.Cls.from_name("qwen3-vl", "Qwen3VL")
        self.instance = self.Qwen3VL()
        logger.newline()
        logger.info(f"Initialized Autograder for day {self.day}")
        
    def grade_batch(self, tasks: list[Task]) -> list[dict]:
        if self.day == 1:
            return self.grade_day1_batch(tasks)
        elif self.day == 2:
            return self.grade_day2_batch(tasks)
        elif self.day == 3:
            return self.grade_day3_batch(tasks)
        elif self.day == 4:
            return self.grade_day4_batch(tasks)
        elif self.day == 5:
            return self.grade_day5_batch(tasks)
        elif self.day == 6:
            return self.grade_day6_batch(tasks)
        elif self.day == 7:
            return self.grade_day7_batch(tasks)
        else:
            raise ValueError(f"Invalid day: {self.day}")
    
    def query_batch(self, tasks: list[Task]) -> list[dict]:
        logger.info(f"Querying batch of {len(tasks)} tasks")
        for task_batch in batched(tasks, self.batch_size):
            try:    
                payload = {
                    task.match.id: {
                        "base64_images": get_all_base64_images(task),
                        "text": task.submit_text or "这是我今天的提交内容"
                    } for task in task_batch
                }
                response = self.instance.run_batch_query_by_base64.remote(payload, system_prompt=get_mission_prompt(self.day))
                save_response_to_tasks(self.day, response, self.use_thinking)
                logger.info(f"Queried batch of {len(task_batch)} tasks")
            except Exception as e:
                logger.error(f"Error while querying batch {task_batch}: {e}")
                continue
        logger.info(f"Queried all tasks")
        
    def grade_day1_batch(self, tasks: list[Task]) -> list[dict]:
        logger.info(f"Grading day 1 batch of {len(tasks)} tasks")
        self.query_batch(tasks)
        for task in tasks:
            if task.match.name != "取个组名吧!":
                task.bonus_score += 10
                task.bonus_review = str(task.bonus_review) + "\n任务: 我们是XXX 已完成, 里程+10"
            task.uni_review = "Triple Uni 暂未评分"
            task.save()
        logger.info(f"Graded day 1 batch of {len(tasks)} tasks")
        return tasks
    
    def grade_day2_batch(self, tasks: list[Task]) -> list[dict]:
        pass
    def grade_day3_batch(self, tasks: list[Task]) -> list[dict]:
        pass
    def grade_day4_batch(self, tasks: list[Task]) -> list[dict]:
        pass
    def grade_day5_batch(self, tasks: list[Task]) -> list[dict]:
        pass
    def grade_day6_batch(self, tasks: list[Task]) -> list[dict]:
        pass
    def grade_day7_batch(self, tasks: list[Task]) -> list[dict]:
        pass
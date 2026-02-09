import modal

from ..models import Match, Task
from ..logger import CustomLogger
from ..configs import AvtivityDates

from .autograder_utils import batched, get_mission_prompt, get_all_base64_images, save_response_to_tasks, get_tripleuni_post_record, remove_empty_payload

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
        elif 2 <= self.day <= 7:
            return self.grade_day2_to_7_batch(tasks)
        else:
            raise ValueError(f"Invalid day: {self.day}")
    
    def llm_batch_grading(self, tasks: list[Task]) -> list[dict]:
        logger.info(f"Querying batch of {len(tasks)} tasks")
        for task_batch in batched(tasks, self.batch_size):
            try:    
                payload = {
                    task.match.id: {
                        "base64_images": get_all_base64_images(task),
                        "text": task.submit_text or "这是我今天的提交内容"
                    } for task in task_batch
                }
                payload = remove_empty_payload(payload, self.day)
                response = self.instance.run_batch_query_by_base64.remote(payload, system_prompt=get_mission_prompt(self.day))
                save_response_to_tasks(self.day, response, self.use_thinking)
                logger.info(f"Queried batch of {len(task_batch)} tasks: {task_batch}")
            except Exception as e:
                logger.error(f"Error while querying batch {task_batch}: {e}")
                continue
        logger.info(f"Queried all tasks")
        
    def query_tripleuni_batch(self, tasks: list[Task], score: int = 10) -> list[dict]:
        release_time_unix = int(AvtivityDates.MISSION_RELEASE_DAY(self.day).timestamp())
        end_time_unix = int(AvtivityDates.MISSION_SUBMIT_END_DAY(self.day).timestamp())
        logger.info(f"Querying tripleuni batch of {len(tasks)} tasks from {release_time_unix} to {end_time_unix}")
        
        for task in tasks:
            task.refresh_from_db()
            try:
                uni_task_completed = get_tripleuni_post_record(task, release_time_unix, end_time_unix)
                if uni_task_completed:
                    task.uni_score = score
                    task.uni_review = "今日已在 Triple Uni 一周CP 板块发帖"
                else:
                    task.uni_score = 0
                    task.uni_review = "今日未在 Triple Uni 一周CP 板块发帖"
            except Exception as e:
                task.uni_score = 0
                task.uni_review = "Triple Uni 评分失败, 请联系你的Mentor"
                logger.error(f"Error while querying tripleuni for task {task}: {e}")
                continue
            task.save()
        logger.info(f"Queried all tasks")
        return tasks
    
    def grade_day1_batch(self, tasks: list[Task]) -> list[dict]:
        logger.info(f"Grading day 1 batch of {len(tasks)} tasks")
        self.query_tripleuni_batch(tasks, score=15)
        self.llm_batch_grading(tasks)
        for task in tasks:
            task.refresh_from_db()
            if task.match.name not in ["取个组名吧!", "取一个组名吧!"]:
                task.bonus_score += 10
                task.bonus_review = str(task.bonus_review) + "\n任务: 我们是XXX 已完成, 里程+10"
            task.scored = True
            task.save()
        logger.info(f"Graded day 1 batch of {len(tasks)} tasks")
        return tasks
    
    def grade_day2_to_7_batch(self, tasks: list[Task]) -> list[dict]:
        logger.info(f"Grading day {self.day} batch of {len(tasks)} tasks")
        self.query_tripleuni_batch(tasks, score=10)
        self.llm_batch_grading(tasks)
        for task in tasks:
            task.refresh_from_db()
            task.scored = True
            task.save()
        logger.info(f"Graded day {self.day} batch of {len(tasks)} tasks")
        return tasks

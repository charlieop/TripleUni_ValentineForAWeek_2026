import pandas as pd
import numpy as np
import abc
import os
from concurrent.futures import ProcessPoolExecutor
from typing import Callable, Literal

# Module-level ref for worker processes (set by _init_scorer_worker)
_worker_scorer = None


def _init_scorer_worker(scorer: "Scorer") -> None:
    global _worker_scorer
    _worker_scorer = scorer


def _score_cell(cell_ij: tuple[int, int]) -> tuple[int, int, float]:
    """Compute score for one (i, j) cell; must be at module level for pickling."""
    i, j = cell_ij
    s = _worker_scorer.score_for_one(
        _worker_scorer.from_df.iloc[i], _worker_scorer.to_df.iloc[j]
    )
    return (i, j, s)

def scaled_sigmoid(x: float) -> float:
    """
    Scaled sigmoid function with a range of 0 to 100.
    """
    return 55 * np.tanh(0.03 * (x - 50))

def identity_transform(x: float) -> float:
    return x-50

class ScorerConfig:
    
    GRADE_MAP = {
        "UG1": 1,
        "UG2": 2,
        "UG3": 3,
        "UG4": 4,
        "UG5": 4.5,
        "MS": 6,
        "PHD": 7,
        "GRAD": 8
    }
    
    # "HK": "香港",
    # "SZ": "深圳",
    # "GD": "广东省",
    # "TW": "台湾",
    # "CN": "中国",
    # "JP_KR": "日韩",
    # "ASIA": "亚洲",
    # "OCEANIA": "大洋洲",
    # "UK": "英国",
    # "EU": "欧洲",
    # "US": "美国",
    # "CA": "加拿大",
    # "NA": "北美洲",
    # "OTHER": "其他",
    
    LOCATION_MAP = {
        "HK": 0,
        "SZ": 1,
        "GD": 1,
        "CN": 2,
        "TW": 2,
        "JP_KR": 2,
        "ASIA": 3,
        "OCEANIA": 3,
        "UK": 4,
        "EU": 4,
        "US": 5,
        "CA": 5,
        "NA": 5,
        "OTHER": 6,
    }
    
    MBTI_MAP = {
        "e": -1,
        "i": 1,
        "s": -1,
        "n": 1,
        "t": -1,
        "f": 1,
        "j": -1,
        "p": 1,
        "x": 0,
    }
    
    def __init__(
        self, 
        base_preference_score: float = 30, # base score for preference
        unqualified_penalty: float = -np.inf, # penalty for unqualified
        preferred_wxid_value: float = 999, # value for preferred_wxid
        
        timezone_difference_base_penalty: float = -2, # base penalty per hour
        timezone_difference_penalty_multiplier_threshold: int = 6, # threshold for penalty multiplier (inclusive)
        timezone_difference_penalty_multiplier: float = 1.25, # multiplier for penalty if time difference is greater than threshold
        
        grade_difference_base_penalty: float = 2.25, # penalty per grade difference
        grade_difference_penalty_multiplier_threshold: int = 3, # threshold for penalty multiplier (inclusive)
        grade_difference_penalty_multiplier: float = 2, # multiplier for penalty if grade difference is greater than threshold
        
        same_location_reward: float = 5, # reward for same location
        same_location_group_reward: float = 3, # reward for same location group
        different_location_group_penalty: float = -1, # penalty for different location group
        
        mbti_transform: Literal["scaled_sigmoid", "identity"] = 'scaled_sigmoid', # a function to transform the mbti score to a range of -50 to 50
        mbti_multiplier: float = 0.25, # multiplier for mbti score
        
        reply_frequency_reward: dict[str, float] = {
            "1": -4, #开启勿扰模式, 闲下来再回
            "2": -1, #攒很多消息, 逐一回复
            "3": 0, #佛系查看, 不定时回复
            "4": 2, #经常看手机, 看到就回
            "5": 5, #一直在线, 基本秒回
        },
        
        
        base_similarity_score: float = 0, # base score for similarity
    ):
        self.base_preference_score = base_preference_score
        self.unqualified_penalty = unqualified_penalty
        self.preferred_wxid_value = preferred_wxid_value
        
        self.timezone_difference_base_penalty = timezone_difference_base_penalty
        self.timezone_difference_penalty_multiplier_threshold = timezone_difference_penalty_multiplier_threshold
        self.timezone_difference_penalty_multiplier = timezone_difference_penalty_multiplier
        
        self.grade_difference_base_penalty = grade_difference_base_penalty
        self.grade_difference_penalty_multiplier_threshold = grade_difference_penalty_multiplier_threshold
        self.grade_difference_penalty_multiplier = grade_difference_penalty_multiplier
        
        self.same_location_reward = same_location_reward
        self.same_location_group_reward = same_location_group_reward
        self.different_location_group_penalty = different_location_group_penalty
        
        self.mbti_transform = scaled_sigmoid if mbti_transform == 'scaled_sigmoid' else identity_transform
        self.mbti_multiplier = mbti_multiplier
        
        self.reply_frequency_reward = reply_frequency_reward
        
        self.base_similarity_score = base_similarity_score
        
        
        

class Scorer(abc.ABC):
    def __init__(self, config: ScorerConfig, from_df: pd.DataFrame, to_df: pd.DataFrame):
        self.config = config
        self.from_df = from_df
        self.to_df = to_df
        self.score_matrix = np.zeros((len(from_df), len(to_df)))
        
    @abc.abstractmethod
    def score_for_one(self, from_applicant: pd.Series, to_applicant: pd.Series) -> float:
        pass
    
    def calculate_score_matrix(self, n_workers: int | None = None) -> np.ndarray:
        n, m = len(self.from_df), len(self.to_df)
        indices = [(i, j) for i in range(n) for j in range(m)]
        if not indices:
            return self.score_matrix
        workers = n_workers or min(os.cpu_count() or 4, len(indices))
        chunksize = max(1, len(indices) // (workers * 4))  # reduce scheduling overhead
        with ProcessPoolExecutor(
            max_workers=workers,
            initializer=_init_scorer_worker,
            initargs=(self,),
        ) as executor:
            for (i, j, score) in executor.map(_score_cell, indices, chunksize=chunksize):
                self.score_matrix[i, j] = score
        return self.score_matrix


#   ['id', 'sex', 'grade', 'wxid, 'school', 'timezone', 'location', 'mbti_ei',
# 'mbti_sn', 'mbti_tf', 'mbti_jp', 'preferred_sex', 'preferred_grades',
# 'preferred_schools', 'max_time_difference', 'same_location_only',
# 'preferred_mbti_ei', 'preferred_mbti_sn', 'preferred_mbti_tf',
# 'preferred_mbti_jp', 'preferred_wxid', 'continue_match', 'comment',
# 'hobbies', 'fav_movies', 'wish', 'why_lamp_remembered_your_name',
# 'weekend_arrangement', 'reply_frequency', 'expectation']

class PreferenceScorer(Scorer):
    def __init__(self, config: ScorerConfig, from_df: pd.DataFrame, to_df: pd.DataFrame):
        super().__init__(config, from_df, to_df)
        
    def score_for_one(self, from_applicant: pd.Series, to_applicant: pd.Series) -> float:
        # if the from_applicant is the preferred_wxid of the to_applicant, return the preferred_wxid_value
        if from_applicant["preferred_wxid"] == to_applicant["wxid"]:
            return self.config.preferred_wxid_value
        
        score = self.config.base_preference_score
                
        # calculate the unqualified penalty
        if (to_applicant["grade"] not in from_applicant["preferred_grades"]) \
            or (to_applicant["school"] not in from_applicant["preferred_schools"]) \
            or ((from_applicant["same_location_only"] == 1) and (to_applicant["location"] != from_applicant["location"])) \
            or (from_applicant["continue_match"] == 0):
            score += self.config.unqualified_penalty
        
        time_a = from_applicant["timezone"]
        time_b = to_applicant["timezone"]
        time_difference = min((time_a - time_b) % 24, (time_b - time_a) % 24)
        
        if time_difference > from_applicant["max_time_difference"]:
            score += self.config.unqualified_penalty

        if score == -np.inf:
            return score
        
        # time zone
        timezone_penalty = self.config.timezone_difference_base_penalty * time_difference
        if time_difference >= self.config.timezone_difference_penalty_multiplier_threshold:
            timezone_penalty *= self.config.timezone_difference_penalty_multiplier
        score += timezone_penalty
        
        # MBTI
        score += self.config.mbti_multiplier * ScorerConfig.MBTI_MAP[from_applicant["preferred_mbti_ei"]] * to_applicant["mbti_ei"]
        score += self.config.mbti_multiplier * ScorerConfig.MBTI_MAP[from_applicant["preferred_mbti_sn"]] * to_applicant["mbti_sn"]
        score += self.config.mbti_multiplier * ScorerConfig.MBTI_MAP[from_applicant["preferred_mbti_tf"]] * to_applicant["mbti_tf"]
        score += self.config.mbti_multiplier * ScorerConfig.MBTI_MAP[from_applicant["preferred_mbti_jp"]] * to_applicant["mbti_jp"]
        
        # location
        if from_applicant["location"] == to_applicant["location"]:
            score += self.config.same_location_reward
        else:
            location_difference = abs(self.config.LOCATION_MAP[from_applicant["location"]] - self.config.LOCATION_MAP[to_applicant["location"]])
            if location_difference == 0:
                score += self.config.same_location_group_reward
            else:
                score += self.config.different_location_group_penalty * location_difference
        
        # grade
        grade_difference = abs(self.config.GRADE_MAP[from_applicant["grade"]] - self.config.GRADE_MAP[to_applicant["grade"]])
        grade_penalty = self.config.grade_difference_base_penalty * grade_difference
        if grade_difference >= self.config.grade_difference_penalty_multiplier_threshold:
            grade_penalty *= self.config.grade_difference_penalty_multiplier
        score += grade_penalty
        
        # reply_frequency
        score += self.config.reply_frequency_reward[to_applicant["reply_frequency"]]
        
        return score


class SimilarityScorer(Scorer):
    def __init__(self):
        pass

    def score_similarity(self, applicant1: pd.Series, applicant2: pd.Series) -> float:
        pass

    
    
import pandas as pd
import numpy as np
import abc
import os
from concurrent.futures import ProcessPoolExecutor
from typing import Literal, Tuple, Optional
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

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
    return x - 50


def cosine_similarity_vector(u: np.ndarray, v: np.ndarray) -> float:
    dot_product = np.dot(u, v)
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)

    return dot_product / (norm_u * norm_v)


def cosine_similarity_matrix(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    dot_product = A @ B.T
    norm_A = np.linalg.norm(A, axis=1, keepdims=True)
    norm_B = np.linalg.norm(B, axis=1, keepdims=True)

    return dot_product / (norm_A * norm_B.T)


class ScorerConfig:
    GRADE_MAP = {
        "UG1": 1,
        "UG2": 2,
        "UG3": 3,
        "UG4": 4,
        "UG5": 4.5,
        "MS": 6,
        "PHD": 7,
        "GRAD": 8,
    }

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
        base_preference_score: float = 0,  # base score for preference
        unqualified_penalty: float = -np.inf,  # penalty for unqualified
        preferred_wxid_value: float = 999,  # value for preferred_wxid
        timezone_difference_base_penalty: float = -2,  # base penalty per hour
        timezone_difference_penalty_multiplier_threshold: int = 6,  # threshold for penalty multiplier (inclusive)
        timezone_difference_penalty_multiplier: float = 1.25,  # multiplier for penalty if time difference is greater than threshold
        grade_difference_base_penalty: float = 2.25,  # penalty per grade difference
        grade_difference_penalty_multiplier_threshold: int = 3,  # threshold for penalty multiplier (inclusive)
        grade_difference_penalty_multiplier: float = 2,  # multiplier for penalty if grade difference is greater than threshold
        same_location_reward: float = 5,  # reward for same location
        same_location_group_reward: float = 3,  # reward for same location group
        different_location_group_penalty: float = -1,  # penalty for different location group
        mbti_transform: Literal[
            "scaled_sigmoid", "identity"
        ] = "scaled_sigmoid",  # a function to transform the mbti score to a range of -50 to 50
        mbti_multiplier: float = 0.25,  # multiplier for mbti score
        reply_frequency_reward: dict[str, float] = {
            "1": -4,  # 开启勿扰模式, 闲下来再回
            "2": -1,  # 攒很多消息, 逐一回复
            "3": 0,  # 佛系查看, 不定时回复
            "4": 2,  # 经常看手机, 看到就回
            "5": 5,  # 一直在线, 基本秒回
        },
        base_similarity_score: float = 0,  # base score for similarity
        hobbies_reward_multiplier: float = 5,  # reward for hobbies bonus
        hobbies_bonus_threshold: float = 0.67,  # threshold for hobbies bonus
        hobbies_bonus_multiplier: float = 1.5,  # multiplier for hobbies bonus
        fav_movies_reward_multiplier: float = 3,  # reward for fav_movies bonus
        fav_movies_bonus_threshold: float = 0.65,  # threshold for fav_movies bonus
        fav_movies_bonus_multiplier: float = 1.5,  # multiplier for fav_movies bonus
        expectation_reward_multiplier: float = 15,  # reward for expectation bonus
        expectation_thresholds: Tuple[float, float] = (
            0.6,
            0.8,
        ),  # thresholds for expectation bonus
        expectation_penalty_multiplier: float = 2,  # multiplier for expectation penalty
        expectation_bonus_multiplier: float = 2,  # multiplier for expectation bonus
        weekend_arrangement_reward_multiplier: float = 7,  # reward for weekend_arrangement bonus
        weekend_arrangement_thresholds: Tuple[float, float] = (
            0.35,
            0.7,
        ),  # thresholds for weekend_arrangement bonus
        weekend_arrangement_penalty_multiplier: float = 2,  # multiplier for weekend_arrangement penalty
        weekend_arrangement_bonus_multiplier: float = 1.5,  # multiplier for weekend_arrangement bonus
        wish_reward_multiplier: float = 5,  # reward for wish bonus
        wish_bonus_threshold: float = 0.65,  # threshold for wish bonus
        wish_bonus_multiplier: float = 1.5,  # multiplier for wish bonus
    ):
        self.base_preference_score = base_preference_score
        self.unqualified_penalty = unqualified_penalty
        self.preferred_wxid_value = preferred_wxid_value

        self.timezone_difference_base_penalty = timezone_difference_base_penalty
        self.timezone_difference_penalty_multiplier_threshold = (
            timezone_difference_penalty_multiplier_threshold
        )
        self.timezone_difference_penalty_multiplier = (
            timezone_difference_penalty_multiplier
        )

        self.grade_difference_base_penalty = grade_difference_base_penalty
        self.grade_difference_penalty_multiplier_threshold = (
            grade_difference_penalty_multiplier_threshold
        )
        self.grade_difference_penalty_multiplier = grade_difference_penalty_multiplier

        self.same_location_reward = same_location_reward
        self.same_location_group_reward = same_location_group_reward
        self.different_location_group_penalty = different_location_group_penalty

        self.mbti_transform = (
            scaled_sigmoid if mbti_transform == "scaled_sigmoid" else identity_transform
        )
        self.mbti_multiplier = mbti_multiplier

        self.reply_frequency_reward = reply_frequency_reward

        self.base_similarity_score = base_similarity_score

        self.hobbies_reward_multiplier = hobbies_reward_multiplier
        self.hobbies_bonus_threshold = hobbies_bonus_threshold
        self.hobbies_bonus_multiplier = hobbies_bonus_multiplier

        self.fav_movies_reward_multiplier = fav_movies_reward_multiplier
        self.fav_movies_bonus_threshold = fav_movies_bonus_threshold
        self.fav_movies_bonus_multiplier = fav_movies_bonus_multiplier

        self.expectation_reward_multiplier = expectation_reward_multiplier
        self.expectation_thresholds = expectation_thresholds
        self.expectation_penalty_multiplier = expectation_penalty_multiplier
        self.expectation_bonus_multiplier = expectation_bonus_multiplier

        self.weekend_arrangement_reward_multiplier = (
            weekend_arrangement_reward_multiplier
        )
        self.weekend_arrangement_thresholds = weekend_arrangement_thresholds
        self.weekend_arrangement_penalty_multiplier = (
            weekend_arrangement_penalty_multiplier
        )
        self.weekend_arrangement_bonus_multiplier = weekend_arrangement_bonus_multiplier

        self.wish_reward_multiplier = wish_reward_multiplier
        self.wish_bonus_threshold = wish_bonus_threshold
        self.wish_bonus_multiplier = wish_bonus_multiplier


class Scorer(abc.ABC):
    def __init__(
        self, config: ScorerConfig, from_df: pd.DataFrame, to_df: pd.DataFrame
    ):
        self.config = config
        self.from_df = from_df
        self.to_df = to_df
        self.score_matrix = np.zeros((len(from_df), len(to_df)))

    @abc.abstractmethod
    def score_for_one(
        self, from_applicant: pd.Series, to_applicant: pd.Series
    ) -> float:
        pass

    def calculate_score_matrix(self, n_workers: int | None = None) -> np.ndarray:
        n, m = len(self.from_df), len(self.to_df)
        indices = [(i, j) for i in range(n) for j in range(m)]
        if not indices:
            return self.score_matrix
        workers = n_workers or min(os.cpu_count() or 4, len(indices))
        logger.info(
            f"Calculating score matrix with {workers} workers, allocating works..."
        )
        with ProcessPoolExecutor(
            max_workers=workers,
            initializer=_init_scorer_worker,
            initargs=(self,),
        ) as executor:
            for i, j, score in tqdm(
                executor.map(_score_cell, indices),
                total=len(indices),
                desc="Calculating score matrix",
            ):
                self.score_matrix[i, j] = score
        return self.score_matrix


class PreferenceScorer(Scorer):
    def __init__(
        self, config: ScorerConfig, from_df: pd.DataFrame, to_df: pd.DataFrame
    ):
        super().__init__(config, from_df, to_df)

    def score_for_one(
        self, from_applicant: pd.Series, to_applicant: pd.Series
    ) -> float:
        # if the from_applicant is the preferred_wxid of the to_applicant, return the preferred_wxid_value
        if from_applicant["preferred_wxid"] == to_applicant["wxid"]:
            return self.config.preferred_wxid_value

        score = self.config.base_preference_score

        # calculate the unqualified penalty
        if (
            (to_applicant["grade"] not in from_applicant["preferred_grades"])
            or (to_applicant["school"] not in from_applicant["preferred_schools"])
            or (
                (from_applicant["same_location_only"] == 1)
                and (to_applicant["location"] != from_applicant["location"])
            )
            or (from_applicant["continue_match"] == 0)
        ):
            score += self.config.unqualified_penalty

        time_a = from_applicant["timezone"]
        time_b = to_applicant["timezone"]
        time_difference = min((time_a - time_b) % 24, (time_b - time_a) % 24)

        if time_difference > from_applicant["max_time_difference"]:
            score += self.config.unqualified_penalty

        if score == -np.inf:
            return score

        # time zone
        timezone_penalty = (
            self.config.timezone_difference_base_penalty * time_difference
        )
        if (
            time_difference
            >= self.config.timezone_difference_penalty_multiplier_threshold
        ):
            timezone_penalty *= self.config.timezone_difference_penalty_multiplier
        score += timezone_penalty

        # MBTI
        score += (
            self.config.mbti_multiplier
            * ScorerConfig.MBTI_MAP[from_applicant["preferred_mbti_ei"]]
            * to_applicant["mbti_ei"]
        )
        score += (
            self.config.mbti_multiplier
            * ScorerConfig.MBTI_MAP[from_applicant["preferred_mbti_sn"]]
            * to_applicant["mbti_sn"]
        )
        score += (
            self.config.mbti_multiplier
            * ScorerConfig.MBTI_MAP[from_applicant["preferred_mbti_tf"]]
            * to_applicant["mbti_tf"]
        )
        score += (
            self.config.mbti_multiplier
            * ScorerConfig.MBTI_MAP[from_applicant["preferred_mbti_jp"]]
            * to_applicant["mbti_jp"]
        )

        # location
        if from_applicant["location"] == to_applicant["location"]:
            score += self.config.same_location_reward
        else:
            location_difference = abs(
                self.config.LOCATION_MAP[from_applicant["location"]]
                - self.config.LOCATION_MAP[to_applicant["location"]]
            )
            if location_difference == 0:
                score += self.config.same_location_group_reward
            else:
                score += (
                    self.config.different_location_group_penalty * location_difference
                )

        # grade
        grade_difference = abs(
            self.config.GRADE_MAP[from_applicant["grade"]]
            - self.config.GRADE_MAP[to_applicant["grade"]]
        )
        grade_penalty = self.config.grade_difference_base_penalty * grade_difference
        if (
            grade_difference
            >= self.config.grade_difference_penalty_multiplier_threshold
        ):
            grade_penalty *= self.config.grade_difference_penalty_multiplier
        score += grade_penalty

        # reply_frequency
        score += self.config.reply_frequency_reward[to_applicant["reply_frequency"]]

        return score


class SimilarityScorer(Scorer):
    def __init__(
        self, config: ScorerConfig, from_df: pd.DataFrame, to_df: pd.DataFrame
    ):
        super().__init__(config, from_df, to_df)

    def score_for_one(
        self, from_applicant: pd.Series, to_applicant: pd.Series
    ) -> float:
        score = self.config.base_similarity_score

        score += self._score_matrix_similarity(
            from_applicant["hobbies_embeddings"],
            to_applicant["hobbies_embeddings"],
            reward_multiplier=self.config.hobbies_reward_multiplier,
            bonus_threshold=self.config.hobbies_bonus_threshold,
            bonus_multiplier=self.config.hobbies_bonus_multiplier,
        )
        score += self._score_matrix_similarity(
            from_applicant["fav_movies_embeddings"],
            to_applicant["fav_movies_embeddings"],
            reward_multiplier=self.config.fav_movies_reward_multiplier,
            bonus_threshold=self.config.fav_movies_bonus_threshold,
            bonus_multiplier=self.config.fav_movies_bonus_multiplier,
        )
        score += self._score_vector_similarity(
            from_applicant["expectation_embeddings"],
            to_applicant["expectation_embeddings"],
            reward_multiplier=self.config.expectation_reward_multiplier,
            thresholds=self.config.expectation_thresholds,
            bonus_multiplier=self.config.expectation_bonus_multiplier,
            penalty_multiplier=self.config.expectation_penalty_multiplier,
        )
        score += self._score_vector_similarity(
            from_applicant["weekend_arrangement_embeddings"],
            to_applicant["weekend_arrangement_embeddings"],
            reward_multiplier=self.config.weekend_arrangement_reward_multiplier,
            thresholds=self.config.weekend_arrangement_thresholds,
            bonus_multiplier=self.config.weekend_arrangement_bonus_multiplier,
            penalty_multiplier=self.config.weekend_arrangement_penalty_multiplier,
        )
        score += self._score_vector_similarity(
            from_applicant["wish_embeddings"],
            to_applicant["wish_embeddings"],
            reward_multiplier=self.config.wish_reward_multiplier,
            thresholds=(None, self.config.wish_bonus_threshold),
            bonus_multiplier=self.config.wish_bonus_multiplier,
            penalty_multiplier=None,
        )
        # score += self._score_vector_similarity(
        #     from_applicant["why_lamp_remembered_your_name_embeddings"],
        #     to_applicant["why_lamp_remembered_your_name_embeddings"],
        #     reward_multiplier=self.config.why_lamp_remembered_your_name_reward_multiplier,
        #     thresholds=None,
        #     bonus_multiplier=None,
        #     penalty_multiplier=None,
        # )

        return score

    def _score_matrix_similarity(
        self,
        from_embeddings: np.ndarray,
        to_embeddings: np.ndarray,
        *,
        reward_multiplier: float,
        bonus_threshold: Optional[float],
        bonus_multiplier: Optional[float],
    ) -> float:
        similarities = cosine_similarity_matrix(from_embeddings, to_embeddings)
        best_matches = np.max(similarities, axis=1)
        scores = best_matches * reward_multiplier
        if bonus_threshold is not None and bonus_multiplier is not None:
            scores[best_matches >= bonus_threshold] *= bonus_multiplier
        return float(np.sum(scores) / np.sqrt(len(best_matches)))

    def _score_vector_similarity(
        self,
        from_embedding: np.ndarray,
        to_embedding: np.ndarray,
        *,
        reward_multiplier: float,
        thresholds: Optional[Tuple[float, Optional[float]]],
        bonus_multiplier: Optional[float],
        penalty_multiplier: Optional[float],
    ) -> float:
        similarity = cosine_similarity_vector(from_embedding, to_embedding)
        score = similarity * reward_multiplier

        lower_threshold = None
        upper_threshold = None
        if thresholds is not None:
            lower_threshold, upper_threshold = thresholds

        if (
            upper_threshold is not None
            and similarity >= upper_threshold
            and bonus_multiplier is not None
        ):
            score *= bonus_multiplier
        elif (
            lower_threshold is not None
            and similarity < lower_threshold
            and penalty_multiplier is not None
        ):
            score *= (similarity - lower_threshold) * penalty_multiplier

        return float(score)

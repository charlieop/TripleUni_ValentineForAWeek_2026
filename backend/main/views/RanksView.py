from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.cache import cache


from ..logger import CustomLogger
from ..mixin import UtilMixin
from .. import configs

logger = CustomLogger("RanksView")


class RanksView(APIView, UtilMixin):
    """
    GET /v1/ranks/?start_pos=1&end_pos=50&type=total|daily
    Returns paginated ranking of CP groups (non-discarded matches).
    - type=total (default): by total score (all tasks)
    - type=daily: by today's score (day computed from FIRST_MISSION_RELEASE)
    Uses UtilMixin for consistent ranking. start_pos/end_pos clamped.
    """

    def _get_ranks(self, rank_type: str) -> tuple[list[dict], int | None]:
        if rank_type == "daily":
            day = self.get_current_day()
            ranking_dict = self.get_daily_ranks(day)
            current_day = day
        else:
            ranking_dict = self.get_all_ranks()
            current_day = None

        match_scores = [
            {
                "id": mid,
                "name": info["group_name"],
                "score": info["total_score"],
                "rank": info["rank"],
            }
            for mid, info in ranking_dict.items()
        ]
        match_scores.sort(key=lambda x: x["score"], reverse=True)
        return match_scores, current_day

    def get(self, request):
        rank_type = request.query_params.get("type", "total")
        if rank_type not in ("total", "daily"):
            rank_type = "total"
            
        try:
            token = self.get_token(request)
            applicant = self.get_applicant_by_token(token)
            match, user_role = self.get_match_by_applicant(applicant)
            match_id = match.id
            logger.info(f"GET ranks type={rank_type} for applicant {applicant.wechat_info.openid}, match_id={match_id}")
        except Exception as e:
            match_id = None
            logger.info(f"GET ranks type={rank_type}")

        cache_key = "match:ranking-list:total" if rank_type == "total" else "match:ranking-list:daily"

        if configs.MAINTENANCE_MODE:
            return Response(
                {"detail": "We are currently undergoing maintenance. Try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        cached = cache.get(cache_key)
        if cached is not None:
            if isinstance(cached, tuple):
                match_scores, current_day = cached
            else:
                match_scores = cached
                current_day = None
        else:
            match_scores, current_day = self._get_ranks(rank_type)
            cache.set(cache_key, (match_scores, current_day), timeout=5 * 60)

        total = len(match_scores)

        try:
            start_pos = max(int(request.query_params.get("start_pos", 1)), 1)
        except (TypeError, ValueError):
            start_pos = 1
        try:
            end_pos = min(int(request.query_params.get("end_pos", total)), total)
        except (TypeError, ValueError):
            end_pos = total

        if total == 0 or start_pos > end_pos:
            payload = {"total": total, "ranks": []}
            if current_day is not None:
                payload["day"] = current_day
            return Response(payload, status=status.HTTP_200_OK)

        payload = {
            "total": total,
            "ranks": match_scores[start_pos - 1 : end_pos],
            "match_id": match_id,
        }
        if current_day is not None:
            payload["day"] = current_day
        return Response(payload, status=status.HTTP_200_OK)

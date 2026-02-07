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
    GET /v1/ranks/?start_pos=1&end_pos=50
    Returns paginated ranking of CP groups (non-discarded matches) by total score.
    Uses UtilMixin.calculate_rank() for consistent ranking. start_pos is clamped to
    max(start_pos, 1), end_pos to min(end_pos, total).
    """
    
    def _get_ranks(self) -> list[dict[str, int, int]]:
        ranking_dict = self.get_all_ranks()
        
        match_scores = [
            {
                "name": info["group_name"],
                "score": info["total_score"],
                "rank": info["rank"],
            }
            for info in ranking_dict.values()
        ]
        match_scores.sort(key=lambda x: x["score"], reverse=True)
        return match_scores

    def get(self, request):
        cache_key = "match:ranking:all"
        
        if configs.MAINTENANCE_MODE:
            return Response(
                {"detail": "We are currently undergoing maintenance. Try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
            
        match_scores = cache.get(cache_key)
        if match_scores is None:
            match_scores = self._get_ranks()
            cache.set(cache_key, match_scores, timeout=900)
            
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
            return Response(
                {"total": total, "ranks": []},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"total": total, "ranks": match_scores[start_pos - 1:end_pos]},
            status=status.HTTP_200_OK,
        )

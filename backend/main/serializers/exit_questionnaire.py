from rest_framework import serializers
from ..models import ExitQuestionnaire


class ExitQuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExitQuestionnaire
        fields = [
            # 关于匹配算法
            "matching_satisfaction",
            "matching_unsatisfied_reason",
            "matching_suggestion",
            # 关于活动任务
            "task_pace",
            "favorite_task",
            "least_favorite_task",
            "task_suggestion",
            "day7_letter_rating",
            # 关于你们
            "heartbeat_moment",
            "knew_before",
            "interaction_frequency",
            "interaction_frequency_other",
            "future_relationship",
            "future_relationship_other",
            "partner_engagement",
            "self_engagement",
            "partner_comment",
            # 跨越时空的书信
            "message_to_partner",
            # Callback
            "lamp_callback",
            # 其他信息
            "participated_last_year",
            "comparison_rating",
            "comparison_comment",
            "discovery_channel",
            "discovery_channel_other",
            "recommendation_likelihood",
            "mentor_rating",
            "accept_callback",
            "message_to_organizer",
            # Timestamps
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

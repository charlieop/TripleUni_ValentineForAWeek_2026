from django.contrib import admin
from ..models import ExitQuestionnaire


@admin.register(ExitQuestionnaire)
class ExitQuestionnaireAdmin(admin.ModelAdmin):
    list_display = [
        "applicant",
        "matching_satisfaction",
        "task_pace",
        "recommendation_likelihood",
        "accept_callback",
        "mentor_rating",
        "created_at",
    ]
    list_filter = [
        "matching_satisfaction",
        "task_pace",
        "knew_before",
        "future_relationship",
        "accept_callback",
        "discovery_channel",
    ]
    search_fields = ["applicant__name", "applicant__wxid"]
    readonly_fields = ["created_at", "updated_at"]
    raw_id_fields = ["applicant"]

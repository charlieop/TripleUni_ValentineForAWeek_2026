from rest_framework import serializers
from ..models import Applicant


class PipeSeparatedListField(serializers.Field):
    """Custom field to handle comma-separated strings as lists"""

    def to_internal_value(self, data):
        if isinstance(data, list):
            return " | ".join(sorted(data))
        return data

    def to_representation(self, value):
        if value:
            return value.split(" | ")
        return []


class ApplicantSerializer(serializers.ModelSerializer):
    # Handle array fields that come as lists but are stored as comma-separated strings
    preferred_grades = PipeSeparatedListField()
    preferred_schools = PipeSeparatedListField()
    hobbies = PipeSeparatedListField()
    fav_movies = PipeSeparatedListField()

    class Meta:
        model = Applicant
        fields = [
            "name",
            "wxid",
            "sex",
            "school",
            "major",
            "email",
            "grade",
            "timezone",
            "location",
            "mbti_ei",
            "mbti_sn",
            "mbti_tf",
            "mbti_jp",
            "hobbies",
            "fav_movies",
            "wish",
            "why_lamp_remembered_your_name",
            "weekend_arrangement",
            "reply_frequency",
            "expectation",
            "preferred_sex",
            "preferred_grades",
            "preferred_schools",
            "max_time_difference",
            "same_location_only",
            "preferred_mbti_ei",
            "preferred_mbti_sn",
            "preferred_mbti_tf",
            "preferred_mbti_jp",
            "preferred_wxid",
            "continue_match",
            "message_to_partner",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

from rest_framework import serializers
from ..models import Task
from .image import ImageSerializer


class GetTaskSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    due = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "day",
            "submit_text",
            "images",
            "basic_completed",
            "basic_score",
            "bonus_score",
            "daily_score",
            "due",
        ]
        read_only_fields = fields

    def get_images(self, obj):
        # Only return non-deleted images
        images = obj.imgs.filter(deleted=False).order_by("created_at")
        return ImageSerializer(images, many=True, context=self.context).data

    def get_due(self, obj):
        return self.context.get("due", False)


class SetTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "submit_text",
        ]

from rest_framework import serializers
from ..models import Image


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ["id", "image_url"]
        read_only_fields = fields

    def get_image_url(self, obj):
        return obj.image.url

    def to_representation(self, instance):
        if instance.deleted:
            return None
        return super().to_representation(instance)

from re import S
from typing import Any


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import (
    ParseError,
    NotFound,
    UnsupportedMediaType,
    ValidationError,
)
from django.http.request import QueryDict
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError as DjangoValidationError

from ..mixin import UtilMixin
from ..models import Image
from ..models.image import VALID_MIME_TYPES, VALID_FILE_EXTENSIONS, SIZE_LIMIT
from ..serializers.image import ImageSerializer


class ImageView(APIView, UtilMixin):
    def get(self, request, day):

        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)

        match, user_role = self.get_match_by_applicant(applicant)
        self.assert_match_not_discarded(match)
        self.assert_day_valid(day)

        task = self.get_task_by_match_and_day(match, day)
        imgs = task.imgs.filter(deleted=False).all()

        serializer = ImageSerializer(imgs, many=True)

        return Response({"data": {"imgs": serializer.data}}, status=status.HTTP_200_OK)

    def post(self, request, day):
        if type(request.data) != QueryDict:
            raise ParseError(
                'Field: "image" is required in body with multipart/form-data'
            )

        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)

        match, user_role = self.get_match_by_applicant(applicant)
        self.assert_match_not_discarded(match)
        self.assert_day_valid(day)

        task = self.get_task_by_match_and_day(match, day)

        imgs = request.data.getlist("images", [])

        if not imgs:
            raise ParseError('At least one image is required in "images" field')

        # Validate and create images
        created_images = []
        errors = []

        for idx, img_file in enumerate[Any](imgs):
            if not isinstance(img_file, UploadedFile):
                errors.append(f"Image {idx + 1}: Invalid file type")
                continue

            # Validate file size
            if img_file.size > SIZE_LIMIT:
                errors.append(
                    f"Image {idx + 1}: File too large. Size should not exceed 5MB"
                )
                continue

            # Validate MIME type
            content_type = getattr(img_file, "content_type", None)
            if not content_type or content_type not in VALID_MIME_TYPES:
                print(f"Warning: Unknown MIME type: {content_type} for image {idx + 1}")
                # Fallback: check file extension
                file_name = getattr(img_file, "name", "").lower()
                if not any(
                    file_name.endswith(ext)
                    for ext in VALID_FILE_EXTENSIONS
                ):
                    errors.append(
                        f"Image {idx + 1}: Unsupported file type. Only JPEG, PNG, JPG, HEIC, HEIF and WebP are allowed."
                    )
                    continue

            # Create Image object
            try:
                image = Image.objects.create(task=task, image=img_file)
                created_images.append(image)
            except DjangoValidationError as e:
                # Handle model validator errors
                error_msg = str(e.message) if hasattr(e, "message") else str(e)
                errors.append(f"Image {idx + 1}: {error_msg}")
            except Exception as e:
                errors.append(f"Image {idx + 1}: Failed to save - {str(e)}")

        if errors:
            # If there are errors, delete any successfully created images
            for img in created_images:
                img.delete()
            raise ValidationError({"detail": errors})

        return Response(
            {"detail": "image upload successfully"}, status=status.HTTP_201_CREATED
        )


class ImageDetailView(APIView, UtilMixin):
    def delete(self, request, day, img_id):
        
        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)

        match, user_role = self.get_match_by_applicant(applicant)
        self.assert_match_not_discarded(match)
        self.assert_day_valid(day)

        task = self.get_task_by_match_and_day(match, day)
        
        image = task.imgs.filter(id=img_id, deleted=False).first()
        if not image:
            raise NotFound("Image not found")
        image.deleted = True
        image.save()
        return Response({"detail": "image deleted successfully"}, status=status.HTTP_200_OK)
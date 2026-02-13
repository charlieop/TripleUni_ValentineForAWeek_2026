from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from ..mixin import UtilMixin
from ..serializers import ExitQuestionnaireSerializer
from ..logger import CustomLogger
from ..configs import AvtivityDates
from ..models import ExitQuestionnaire

logger = CustomLogger("exit_questionnaire")


class ExitQuestionnaireView(APIView, UtilMixin):

    def get(self, request):
        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)
        logger.info(f"GET: {applicant.wechat_info.openid}")

        try:
            questionnaire = ExitQuestionnaire.objects.get(applicant=applicant)
        except ExitQuestionnaire.DoesNotExist:
            raise NotFound({"detail": "Exit questionnaire not found"})

        return Response(
            {
                "data": {
                    "form_data": ExitQuestionnaireSerializer(questionnaire).data,
                }
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        AvtivityDates.assert_valid_exit_questionnaire_period()

        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)

        logger.info(f"POST: {applicant.wechat_info.openid}")

        # Check if questionnaire already exists
        try:
            existing_questionnaire = ExitQuestionnaire.objects.get(
                applicant=applicant
            )
            logger.info(
                f"Updating existing exit questionnaire for: {applicant.wechat_info.openid}"
            )
        except ExitQuestionnaire.DoesNotExist:
            existing_questionnaire = None
            logger.info(
                f"Creating new exit questionnaire for: {applicant.wechat_info.openid}"
            )

        serializer = ExitQuestionnaireSerializer(
            instance=existing_questionnaire,
            data=request.data,
            partial=existing_questionnaire is not None,
        )
        serializer.is_valid(raise_exception=True)

        serializer.save(applicant=applicant)

        logger.info(
            f"Saved exit questionnaire for: {applicant.wechat_info.openid}"
        )

        return Response(
            {"data": {"success": True}}, status=status.HTTP_200_OK
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from ..mixin import UtilMixin
from ..serializers import ApplicantSerializer
from ..logger import CustomLogger
from ..configs import AvtivityDates

logger = CustomLogger("applicant")


class ApplicantView(APIView, UtilMixin):

    def get(self, request):
        # AvtivityDates.assert_valid_application_period()

        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)
        logger.info(f"GET: {applicant.wechat_info.openid}")

        return Response(
            {
                "data": {
                    "paid": applicant.has_paid(),
                    "form_data": ApplicantSerializer(applicant).data,
                }
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        AvtivityDates.assert_valid_application_period()

        # Get token and wechat_info
        token = self.get_token(request)
        wechat_info = self.get_wechat_info_by_token(token)

        logger.info(f"POST: {wechat_info.openid}")

        # Check if applicant already exists
        try:
            existing_applicant = self.get_applicant_by_token(token)
            logger.info(f"Updating existing applicant for: {wechat_info.openid}")
        except NotFound:
            existing_applicant = None
            logger.info(f"Creating new applicant for: {wechat_info.openid}")

        # Validate and serialize the data
        serializer = ApplicantSerializer(
            instance=existing_applicant,
            data=request.data,
            partial=existing_applicant is not None,
        )
        serializer.is_valid(raise_exception=True)

        applicant = serializer.save(wechat_info=wechat_info)

        logger.info(f"Saved applicant for: {wechat_info.openid}")

        return Response(
            {"data": {"paid": applicant.has_paid()}}, status=status.HTTP_200_OK
        )

    def delete(self, request):
        AvtivityDates.assert_valid_application_period()

        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)

        logger.warning(f"DELETE: {applicant.wechat_info.openid}")

        applicant.quitted = True
        applicant.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

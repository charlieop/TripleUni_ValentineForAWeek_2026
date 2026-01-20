from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from ..mixin import UtilMixin, Gone
from ..serializers import ApplicantSerializer


class ApplicantView(APIView, UtilMixin):
    
    def get(self, request):
        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)
        
        return Response(
            {"data": {"paid": applicant.has_paid(), "form_data": ApplicantSerializer(applicant).data}}, status=status.HTTP_200_OK
        )
    
    def post(self, request):
        # Get token and wechat_info
        token = self.get_token(request)
        wechat_info = self.get_wechat_info_by_token(token)

        # Check if applicant already exists
        try:
            existing_applicant = self.get_applicant_by_token(token)
        except NotFound:
            existing_applicant = None

        # Validate and serialize the data
        serializer = ApplicantSerializer(
            instance=existing_applicant,
            data=request.data,
            partial=existing_applicant is not None,
        )
        serializer.is_valid(raise_exception=True)
        
        applicant = serializer.save(wechat_info=wechat_info)
        
        return Response(
            {"data": {"paid": applicant.has_paid()}}, status=status.HTTP_200_OK
        )
        
    def delete(self, request):
        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)
        applicant.quitted = True
        applicant.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
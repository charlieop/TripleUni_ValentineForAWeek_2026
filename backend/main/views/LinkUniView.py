import requests
import json

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..mixin import UtilMixin
from ..logger import CustomLogger

logger = CustomLogger("LinkUni")

API_URL = "https://eo.api.tripleuuunnniii.com/v4/valentine/getuserinfo.php"

with open(settings.BASE_DIR / "SECRETS.json") as f:
    secrets = json.load(f)
    UNI_APPID = secrets["UNI_APPID"]
    UNI_APPKEY = secrets["UNI_APPKEY"]

class LinkUniView(APIView, UtilMixin):
    
    def _generate_payload(self, user_email: str) -> dict:
        return f"appid={UNI_APPID}&appkey={UNI_APPKEY}&user_email={user_email}"
    
    def post(self, request):
        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)
        
        if applicant.linked_uni:
            return Response({"detail": "Uni already linked"}, status=status.HTTP_200_OK)

        user_email = applicant.email
        
        response = requests.request("POST", API_URL, data=self._generate_payload(user_email), headers={"Content-Type": "application/x-www-form-urlencoded"})
        data = response.json()
        
        if "code" not in data:
            return Response({"detail": "Request to Triple Uni API failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if data["code"] != 200:
            return Response({"detail": data["msg"]}, status=status.HTTP_401_UNAUTHORIZED)
        
        applicant.linked_uni = True
        applicant.save()
        
        return Response({"detail": "Uni linked successfully"}, status=status.HTTP_200_OK)
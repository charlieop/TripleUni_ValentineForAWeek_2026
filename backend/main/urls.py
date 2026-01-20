from django.urls import path
from .views.index import index
from .views.WeChatLoginView import wechat_oauth_view
from .views.ApplicantView import ApplicantView

app_name = "main"

urlpatterns = [
    path("", index, name="index"),
    path("oauth/wechat/", wechat_oauth_view, name="wechat_oauth"),
    
    path("applicants/", ApplicantView.as_view(), name="submit_applicant"),
]

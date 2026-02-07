from django.urls import path
from .views.WeChatLoginView import wechat_oauth_view
from .views.ApplicantView import ApplicantView
from .views.MatchView import (
    MatchResultDetailView,
    MatchDetailView,
)
from .views.TaskView import (
    TaskDetailView,
    TaskVisibilityView,
    SecretTaskView
)
from .views.MissionView import MissionDetailView
from .views.ImageView import (
    ImageView,
    ImageDetailView,
)
from .views.WeChatPaymentView import WeChatPaymentView
from .views.StatusView import StatusView
from .views.LinkUniView import LinkUniView
from .views.RanksView import RanksView


app_name = "main"

urlpatterns = [
    path("oauth/wechat/", wechat_oauth_view, name="wechat_oauth"),
    path("applicants/", ApplicantView.as_view(), name="submit_applicant"),
    
    # Match result endpoints
    path(
        "match-result/",
        MatchResultDetailView.as_view(),
        name="match_result_detail",
    ),
    
    # Match detail endpoints
    path("match/", MatchDetailView.as_view(), name="match_detail"),
    
    # Task endpoints
    path("tasks/<int:day>/", TaskDetailView.as_view(), name="task_detail"),
    path(
        "tasks/<int:day>/visibility/",
        TaskVisibilityView.as_view(),
        name="task_visibility",
    ),

    # Mission endpoints
    path("missions/<int:day>/", MissionDetailView.as_view(), name="mission_detail"),
    
    # Image endpoints
    path("tasks/<int:day>/imgs/", ImageView.as_view(), name="image_list"),
    path("tasks/<int:day>/imgs/<uuid:img_id>/", ImageDetailView.as_view(), name="image_detail"),
    path("tasks/secret/", SecretTaskView.as_view(), name="secret_task"),
    
    # Payment endpoints
    path("payment/wechat/", WeChatPaymentView.as_view(), name="wechat_payment"),
    
    # Status endpoints
    path("status/", StatusView.as_view(), name="status"),
    
    # Link Uni endpoints
    path("link-uni/", LinkUniView.as_view(), name="link_uni"),

    # Ranks (leaderboard) - public, no auth
    path("ranks/", RanksView.as_view(), name="ranks"),
]

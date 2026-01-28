# Import all admin classes to register them
from .applicant import ApplicantAdmin
from .wechat_info import WeChatInfoAdmin
from .payment_record import PaymentRecordAdmin
from .mentor import MentorAdmin
from .match import MatchAdmin
from .task import TaskAdmin
from .image import ImageAdmin
from .mission import MissionAdmin
from .token import TokenAdmin
from .config import ConfigAdmin
from .system_actions import SystemActionsAdmin

from . import cache_management
from . import cache_management_menu

__all__ = [
    "ApplicantAdmin",
    "WeChatInfoAdmin",
    "PaymentRecordAdmin",
    "MentorAdmin",
    "MatchAdmin",
    "TaskAdmin",
    "ImageAdmin",
    "MissionAdmin",
    "TokenAdmin",
    "ConfigAdmin",
    "SystemActionsAdmin",
    "CacheManagementAdmin",
]

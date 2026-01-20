from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(WeChatInfo)
admin.site.register(Token)
admin.site.register(PaymentRecord)
admin.site.register(Applicant)
admin.site.register(Mentor)
admin.site.register(Match)
admin.site.register(Task)
admin.site.register(Image)
admin.site.register(Mission)
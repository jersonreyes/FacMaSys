from django.contrib import admin
from .models import ActivityLog, StoreInfo, EmailNotification

admin.site.register(ActivityLog)
admin.site.register(StoreInfo)
admin.site.register(EmailNotification)
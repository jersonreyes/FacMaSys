from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *


admin.site.site_header = 'FacMaSys Admin'
admin.site.register(Announcements)
admin.site.register(Announcements_DepartmentHead)
admin.site.register(Announcements_ResearchCoord)
admin.site.register(Announcements_ExtensionCoord)
from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *

admin.site.site_header = 'FacMaSys Admin'
admin.site.register(Feeds)
admin.site.register(Feeds_DepartmentHead)
admin.site.register(Feeds_ResearchCoord)
admin.site.register(Feeds_ExtensionCoord)
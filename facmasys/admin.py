from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *

admin.site.site_header = 'FacMaSys Admin'
admin.site.register(Research)
admin.site.register(Research_Presented)
admin.site.register(Research_Published)

admin.site.register(Subjects)
admin.site.register(Subjects_Taught)

admin.site.register(ExtensionService)
admin.site.register(ExtensionService_OfferedPrograms)
admin.site.register(ExtensionService_Collaborators)

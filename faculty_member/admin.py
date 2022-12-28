from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ExtensionService_Collaborators)
admin.site.register(ExtensionService_OfferedPrograms)
admin.site.register(ExtensionService)

admin.site.register(Research_Presented)
admin.site.register(Research_Published)
admin.site.register(Research)

admin.site.register(Subjects_Taught)
admin.site.register(Subjects)

# admin.site.register(Users)
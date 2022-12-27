from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType 
from user.models import User
 
new_group, created = Group.objects.get_or_create(name ='admin')
# Code to add permission to group
ct = ContentType.objects.get_for_model(User)

new_group, created = Group.objects.get_or_create(name ='superadmin')
# Code to add permission to group
ct = ContentType.objects.get_for_model(User)
 
# If I want to add 'Can go Haridwar' permission to level0 ?





# Create your models here.

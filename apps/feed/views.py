import json

import pandas as pd
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from apps.reports.models import Notifications

from .models import *

Profile = apps.get_model('user', 'Profile')

# Create your views here.
@login_required
def index(request):
    
    # Notifications
    notifications = Notifications.objects.filter(user=request.user)

    # Announcement Objects
    feeds = Feeds.objects.all()
    
    field_name = 'user_role'
    obj = Profile.objects.first()
    field_object = Profile._meta.get_field(field_name)
    field_value = field_object.value_from_object(obj)
    print('field value: ', field_value)
    
    
    context={
        'state':'feed',
        'notifications': notifications,
        
        # Announcement Objects
        'feeds':feeds,
        'user_types':field_value,
    }
    return render(request, 'feed/index.html', context)
    
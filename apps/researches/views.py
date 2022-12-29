import json

import pandas as pd
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q

from apps.reports.models import Notifications
from apps.user.models import Profile
from facmasys.models import *


# Create your views here.
@login_required
def index(request):  
    # Notifications
    notifications = Notifications.objects.filter(user=request.user)
    # Summary Research Object
    if 'q' in request.GET:
        all_researches = Research.objects.filter(Q(research_title__icontains=request.GET['q']) | Q(abstract__icontains=request.GET['q'])).order_by('-date_added')
    else:
        all_researches = Research.objects.order_by('-date_added')
    users = Profile.objects.all()
    context={
        'state':'researches',
        'notifications':notifications,
        'users':users,
        # Summary Research Object
        'all_researches': all_researches,
    }
    return render(request, 'researches/index.html', context)


@login_required
def get_research(request, id): # May include more arguments depending on URL parameters
    research = list(Research.objects.filter(id = id).values())[0]
    user = list(Profile.objects.filter(id = research["faculty_id_id"]).values())[0]
    response={
        'research': research,
        'user': user,
    }
    return JsonResponse(dict(response), safe=False)

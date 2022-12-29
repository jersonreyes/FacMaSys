import json

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from apps.reports.models import Notifications
from facmasys.models import *


# Create your views here.
@login_required
def index(request):
    # Default graph view - Sales of current year grouped by month
    time = 'year'    
    # Notifications
    notifications = Notifications.objects.filter(user=request.user)

    # Summary Research Object
    all_researches = Research.objects.all()
    
    context={
        'time':time,
        'state':'researches',
        'notifications':notifications,

        # Summary Research Object
        'all_researches': all_researches,
    }
    return render(request, 'researches/index.html', context)

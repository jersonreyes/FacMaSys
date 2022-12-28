from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.reports.models import Notifications


# Create your views here.
@login_required
def index(request):
    # Notifications
    notifications = Notifications.objects.filter(user=request.user)
    
    context={
        'state':'researches',
        'notifications':notifications,
    }
    return render(request, 'researches/index.html', context)
    
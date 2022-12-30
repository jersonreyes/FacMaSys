from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.reports.models import Notifications
from facmasys.models import Research
from apps.user.models import Profile
# Create your views here.
@login_required
def index(request):    
    # Notifications
    notifications = Notifications.objects.filter(user=request.user)
    research_count = Research.objects.all().count()
    faculty_count = Profile.objects.filter(user_role="faculty").count()
    context={
        'state':'dashboard',
        'notifications':notifications,
        'research_count':research_count,
        'faculty_count':faculty_count,
    }
    return render(request, 'dashboard/index1.html', context)
    
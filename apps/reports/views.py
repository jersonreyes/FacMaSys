from time import localtime, strftime

import matplotlib
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django_tables2.export.views import ExportMixin
from matplotlib import pyplot as plt

from apps.reports.models import Notifications
from apps.user.filters import FacultyFilter
from apps.user.tables import FacultyTable
from facmasys.utils import ExportPDF

from .filters import *
from .models import ActivityLog
from .tables import *

matplotlib.use('Agg')


# Create your views here.
@login_required
def view_settings(request):
    context = {'notifications':Notifications.objects.filter(user=request.user)}
    return render(request, 'reports/setting.html', context)


class ActivityView(LoginRequiredMixin, SingleTableMixin, ExportMixin, ExportPDF, FilterView):
    table_class = ActivityTable
    filterset_class = ActivityFilter
    queryset = ActivityLog.objects.values('id','datetime','type','location','user__username','message')
    paginate_by = 10
    state = 'settings'
    label = 'Settings'
    export_formats = ('xlsx','csv','pdf')
    exclude_columns = ('id',)
    export_name = f"Activity_Log_Report_{strftime('%Y-%m-%d', localtime())}"
    dataset_kwargs = {"title": "Activity Log"}
    
    def get_context_data(self, *args, **kwargs):
        context = super(ActivityView, self).get_context_data(*args, **kwargs)
        context['notifications'] = Notifications.objects.filter(user=self.request.user)
        return context
    
    def get_template_names(self):

        return 'partials/table.html' if self.request.htmx else 'reports/activity_log.html'
    
    def get_queryset(self):
        return ActivityLog.objects.values('id','datetime','type','location','user__username','message') if self.request.user.is_superuser else ActivityLog.objects.values('id','datetime','type','location','user__username','message').filter(user=self.request.user)


def delete_notification(request,pk):
    notif = Notifications.objects.get(id=pk)
    notif.delete()
    
    return redirect('dashboard-index')

class view_reports(LoginRequiredMixin, SingleTableMixin, ExportMixin, ExportPDF, FilterView):
    table_class = FacultyTable
    filterset_class = FacultyFilter
    queryset = User.objects.filter(profile__user_role='faculty').values('id','first_name','last_name','username','email','profile')
    paginate_by = 10
    state = 'reports'
    label = 'Faculty'
    export_formats = ('xlsx','pdf')
    export_name = f"Faculty_List_Report_{strftime('%Y-%m-%d', localtime())}"
    dataset_kwargs = {"title": "Faculty"}
    
    def get_template_names(self):

        return 'partials/table.html' if self.request.htmx else 'reports/index.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.user_role == 'faculty':
            return redirect('dashboard-index')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        if (search := request.GET.get('q')) != None:
            self.label += f' filtered by {search}'
            
        return super().get(request)

def delete_all_notification(request):
    notif = Notifications.objects.filter(user=request.user)
    notif.delete()
    
    return redirect('dashboard-index')

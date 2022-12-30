from django.contrib import admin
from .models import ActivityLog
from facmasys.utils import add_activity, render_to_pdf
import pandas as pd

class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('datetime','type','location','user','message')
    list_filter = ('type','location')
    search_fields = ('user','type','location')
    actions = ('export_pdf',)
    
    @admin.action(description='Export as PDF')
    def export_pdf(self, request, queryset):
        df = pd.DataFrame.from_records(queryset.values('datetime','type','location','user','message'))
        df.columns = [col.replace('_',' ').title() for col in df.columns]
        context = {
            'title':'Activity Log Report',
            'user':request.user.username,
            'table':df.to_html(classes=['table', 'table-striped', 'bg-white', 'text-center'],index=False)
        }
        add_activity(logged_user=request.user,activity_type='EXPORT PDF',activity_location='ACTIVITY LOG',activity_message=f"Activity_Log_Report.pdf was exported")
        
        return render_to_pdf(request,'reports/report.html', f'Activity_Log_Report.pdf', context)
    
    
admin.site.register(ActivityLog, ActivityLogAdmin)
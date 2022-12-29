from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
import pandas as pd
from facmasys.utils import render_to_pdf, add_activity

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','phone','role')
    actions = ['export_pdf']
    
    @admin.display(empty_value='None')
    def phone(self, obj):
         return obj.profile.phone
     
    @admin.display(empty_value='None')
    def role(self, obj):
         return obj.profile.user_role
     
    @admin.action(description='Export as PDF')
    def export_pdf(self, request, queryset):
        df = pd.DataFrame.from_records(queryset.values('first_name','last_name','email','profile__phone','profile__user_role'))
        df.columns = [col.replace('_',' ').title() for col in df.columns]
        context = {
            'title':'User List Report',
            'user':request.user.username,
            'table':df.to_html(classes=['table', 'table-striped', 'bg-white', 'text-center'],index=False)
        }
        add_activity(logged_user=request.user,activity_type='EXPORT PDF',activity_location='USER',activity_message=f"User_List_Report.pdf was exported")
        
        return render_to_pdf(request,'reports/report.html', f'User_List_Report.pdf', context)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Profile)
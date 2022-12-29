from django.contrib import admin
from .models import *
import pandas as pd
from facmasys.utils import render_to_pdf, add_activity

# Register your models here.
class ExtensionServiceCollaboratorAdmin(admin.ModelAdmin):
    list_display = ('name','position')
    list_filter = ('position',)
    search_fields = ('name','position')
    actions = ('export_pdf',) 
    
    @admin.action(description='Export as PDF')
    def export_pdf(self, request, queryset):
        df = pd.DataFrame.from_records(queryset.values('name','position'))
        df.columns = [col.replace('_',' ').title() for col in df.columns]
        context = {
            'title':'Extension Service Collaborator Report',
            'user':request.user.username,
            'table':df.to_html(classes=['table', 'table-striped', 'bg-white', 'text-center'],index=False)
        }
        add_activity(logged_user=request.user,activity_type='EXPORT PDF',activity_location='EXTENSION SERVICE COLLABORATOR',activity_message=f"Extension_Service_Collaborator_List_Report.pdf was exported")

        return render_to_pdf(request,'reports/report.html', f'Extension_Service_Collaborator_List_Report.pdf', context)


class ExtensionServiceOfferedProgramAdmin(admin.ModelAdmin):
    list_display = ('program_name','description')
    search_fields = ('program_name',)
    actions = ('export_pdf',) 
    
    @admin.action(description='Export as PDF')
    def export_pdf(self, request, queryset):
        df = pd.DataFrame.from_records(queryset.values('program_name','description'))
        df.columns = [col.replace('_',' ').title() for col in df.columns]
        context = {
            'title':'Extension Service Offered Program Report',
            'user':request.user.username,
            'table':df.to_html(classes=['table', 'table-striped', 'bg-white', 'text-center'],index=False)
        }
        add_activity(logged_user=request.user,activity_type='EXPORT PDF',activity_location='EXTENSION SERVICE OFFERED PROGRAM',activity_message=f"Extension_Service_Offered_Program_List_Report.pdf was exported")

        return render_to_pdf(request,'reports/report.html', f'Extension_Service_Offered_Program_List_Report.pdf', context)
    

class ExtensionServiceAdmin(admin.ModelAdmin):
    list_display = ('faculty','name','email','contact_no','extension_head','address')
    search_fields = ('faculty','name','email','contact_no','extension_head','address')
    actions = ('export_pdf',) 
    
    @admin.display(empty_value='None')
    def faculty(self, obj):
         return obj.faculty_id.username
    
    @admin.action(description='Export as PDF')
    def export_pdf(self, request, queryset):
        df = pd.DataFrame.from_records(queryset.values('faculty','name','email','contact_no','extension_head','address'))
        df.columns = [col.replace('_',' ').title() for col in df.columns]
        context = {
            'title':'Extension Services Report',
            'user':request.user.username,
            'table':df.to_html(classes=['table', 'table-striped', 'bg-white', 'text-center'],index=False)
        }
        add_activity(logged_user=request.user,activity_type='EXPORT PDF',activity_location='EXTENSION SERVICE',activity_message=f"Extension_Service_List_Report.pdf was exported")

        return render_to_pdf(request,'reports/report.html', f'Extension_Service_List_Report.pdf', context)
    

class ResearchAdmin(admin.ModelAdmin):
    list_display = ('faculty','research_title','research_progress','research_area','degree_level','researcher_school')
    list_filter = ('research_progress','research_area','degree_level')
    search_fields = ('faculty','research_title','research_progress','research_area','degree_level','researcher_school')
    actions = ('export_pdf',) 
    
    @admin.display(empty_value='None')
    def faculty(self, obj):
         return obj.faculty_id.username
    
    @admin.action(description='Export as PDF')
    def export_pdf(self, request, queryset):
        df = pd.DataFrame.from_records(queryset.values('faculty','research_title','research_progress','research_area','degree_level','researcher_school'))
        df.columns = [col.replace('_',' ').title() for col in df.columns]
        context = {
            'title':'Research Report',
            'user':request.user.username,
            'table':df.to_html(classes=['table', 'table-striped', 'bg-white', 'text-center'],index=False)
        }
        add_activity(logged_user=request.user,activity_type='EXPORT PDF',activity_location='RESEARCH',activity_message=f"Research_List_Report.pdf was exported")

        return render_to_pdf(request,'reports/report.html', f'Research_List_Report.pdf', context)
    

class ResearchPresentedAdmin(admin.ModelAdmin):
    list_display = ('faculty','research_title','research_progress','research_area','degree_level','researcher_school')
    list_filter = ('research_progress','research_area','degree_level')
    search_fields = ('faculty','research_title','research_progress','research_area','degree_level','researcher_school')
    actions = ('export_pdf',) 
    
    @admin.display(empty_value='None')
    def faculty(self, obj):
         return obj.faculty_id.username
    
    @admin.action(description='Export as PDF')
    def export_pdf(self, request, queryset):
        df = pd.DataFrame.from_records(queryset.values('faculty','research_title','research_progress','research_area','degree_level','researcher_school'))
        df.columns = [col.replace('_',' ').title() for col in df.columns]
        context = {
            'title':'Research Report',
            'user':request.user.username,
            'table':df.to_html(classes=['table', 'table-striped', 'bg-white', 'text-center'],index=False)
        }
        add_activity(logged_user=request.user,activity_type='EXPORT PDF',activity_location='RESEARCH',activity_message=f"Research_List_Report.pdf was exported")

        return render_to_pdf(request,'reports/report.html', f'Research_List_Report.pdf', context)




admin.site.register(ExtensionService_Collaborators, ExtensionServiceCollaboratorAdmin)
admin.site.register(ExtensionService_OfferedPrograms, ExtensionServiceOfferedProgramAdmin)
admin.site.register(ExtensionService, ExtensionServiceAdmin)

admin.site.register(Research, ResearchAdmin)
admin.site.register(Research_Presented)
admin.site.register(Research_Published)

admin.site.register(Subjects_Taught)
admin.site.register(Subjects)

# admin.site.register(Users)
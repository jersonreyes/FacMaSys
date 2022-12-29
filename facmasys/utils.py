from time import sleep
import pandas as pd
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from weasyprint import HTML
from apps.reports.models import ActivityLog


def render_to_pdf(request, template_src, filename, context_dict={}, scale=1.0):
    # Find and render template
    html = render_to_string(template_src,context_dict)
    pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(zoom=scale)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    
    return response


class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["HX-Redirect"] = self["Location"]

    status_code = 200


class ExportPDF:
    label = 'Title'
    exclude_columns = None
    export_name = 'Export.pdf'
        
    def render_to_response(self, context, **kwargs):
        if self.request.GET.get('_export') == 'pdf':
            df = pd.DataFrame.from_records(self.get_table_data())
            if df.shape[0] != 0:
                if columns := self.exclude_columns:
                    for column in columns:
                        df.drop(column, inplace=True, axis=1)
                df.columns = [col.replace('_',' ').title() for col in df.columns]
                context['title'] = self.label
                context['user'] = self.request.user.username
                context['table'] = df.to_html(classes=['table', 'table-striped', 'bg-white', 'text-center'],index=False)
                # add_activity(logged_user=self.request.user,activity_type='EXPORT PDF',activity_location=self.label,activity_message=f"{self.export_name}.pdf was exported")
                
                return render_to_pdf(self.request,'reports/report.html', f'{self.export_name}.pdf', context)
            messages.warning(self.request,"Nothing to export.")
            
        return super().render_to_response(context, **kwargs)


def add_activity(logged_user, activity_type, activity_location, activity_message):
    activity = ActivityLog.objects.create(type=activity_type,location=activity_location,user=logged_user,message=activity_message) 
    return activity.save()

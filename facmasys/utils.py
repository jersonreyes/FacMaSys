import json
from time import sleep

import pandas as pd
import requests
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from weasyprint import HTML

from apps.reports.models import ActivityLog, StoreInfo

# Shopify REST API
api_url = 'https://facmasyspos.myshopify.com/admin/api/2022-10/'
sess = requests.Session()
sess.headers.update({
    "X-Shopify-Access-Token": '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',
    "Content-Type": "application/json" 
})


def render_to_pdf(request, template_src, filename, context_dict={}, scale=1.0):
    storeinfo = StoreInfo.objects.first()
    context={'storeinfo':storeinfo}
    context_dict|=context
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
                add_activity(logged_user=self.request.user,activity_type='EXPORT PDF',activity_location=self.label,activity_message=f"{self.export_name}.pdf was exported")
                
                return render_to_pdf(self.request,'reports/report.html', f'{self.export_name}.pdf', context)
            messages.warning(self.request,"Nothing to export.")
            
        return super().render_to_response(context, **kwargs)


def check_api_limit(response):
    limit = response.headers['X-Shopify-Shop-Api-Call-Limit'].split("/")
    if int(limit[0]) >= int(limit[1])-1:
        sleep(2)
    
    return f'(API Limit: {limit[0]} of {limit[1]})'


def get_api_json(endpoint):
    try:
        resp = sess.get(api_url + endpoint)
        print(check_api_limit(resp))
        
        # pp = sess.get(api_url + 'products.json?limit=1')
        # print(pp.json())
        
        # endpoint = 'products.json?limit=250&fields=id'
        # prods = sess.get(api_url + endpoint).json()
        # df = pd.DataFrame(prods['products'])
        
        # for p in df['id']:
        #     endpoint = f'products/{p}/metafields.json'
        #     payload = {"metafield":{"namespace":"custom","key":"low_stock","value":0,"type":"number_integer"}}
        #     pos = post_api_json(endpoint,payload)
        #     print(pos)

        return resp.json()
    except ConnectionError:
        return redirect('inventory-product')


def post_api_json(endpoint, payload):
    resp = sess.post(api_url + endpoint,json=payload)
    print(check_api_limit(resp))
    
    return resp.json()


def put_api_json(endpoint, payload):
    resp = sess.put(api_url + endpoint,json=payload)
    print(check_api_limit(resp))
    
    return resp.json()


# Add Peso currency logo to value
def to_peso(amount):
    peso = u'\u20B1'
    return '{:>10}'.format(peso + ' {:>.2f}'.format(float(amount)))


def to_peso_safe(amount):
    return f"<span>&#8369;</span>{float(amount):,.2f}"


def add_activity(logged_user, activity_type, activity_location, activity_message):
    activity = ActivityLog.objects.create(type=activity_type,location=activity_location,user=logged_user,message=activity_message) 
    return activity.save()

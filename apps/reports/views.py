import base64
import datetime
import json
from datetime import datetime, timedelta
from time import localtime, strftime

import matplotlib
import pandas as pd
import seaborn as sns
import xlwt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django_tables2.export.views import ExportMixin

from apps.reports.models import Notifications
from apps.sales.models import Order, OrderProduct
from facmasys.utils import (ExportPDF, add_activity, get_api_json,
                            render_to_pdf, to_peso_safe)

from .filters import *
from .models import ActivityLog
from .tables import *

matplotlib.use('Agg')
from datetime import timedelta
from io import BytesIO

from django.core.mail import send_mail
from django.utils import timezone
from django_q.models import Schedule
from django_q.tasks import async_task, schedule
from matplotlib import pyplot as plt

from .forms import NotificationForm, StoreForm
from .models import EmailNotification, StoreInfo


# Create your views here.
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


# PDF Reports ------------------------------------------------------------------
@login_required
def exportcustomer_pdf(request, pk):
    storeinfo = StoreInfo.objects.first()
    customer = Order.objects.get(id=pk)
    filename = f'Invoice_{customer.invoice_number}.pdf'
    context = {
        "storeinfo":storeinfo,
        "customer": customer,
        "products": customer.products.all(),
        "services": customer.services.all(),
        "user": request.user.username,
        "title":filename,
    }
    add_activity(logged_user=request.user,activity_type='DOWNLOAD PDF',activity_location='INVOICE',activity_message=f'Invoice_{customer.invoice_number}.pdf has been downloaded')
    return render_to_pdf(request, 'reports/invoice.html', filename, context, 0.8)


@login_required
def exportproduct_pdf(request):
    storeinfo = StoreInfo.objects.first()
    # Get Products
    if 'products' in request.session:
        products = pd.DataFrame(request.session['products'])
    else:
        endpoint = 'products.json?fields=id,title,product_type,vendor,tags,variants&status=active'
        products = pd.DataFrame(get_api_json(endpoint)['products'])
        products['price'] = products.apply(lambda row: f"<span>&#8369;</span> {float(row.variants[0]['price']):,.2f}", axis=1)
        products['quantity'] = products.apply(lambda row: row.variants[0]['inventory_quantity'], axis=1)
    # Modify Product Columns
    # products['images'] = products.apply(lambda row: f"<img class='image' src='{row.images[0]['src']}'>", axis=1)  # removed images due to pdf export taking a long time to finish.
    # Change columns arrangement
    products = products[['id','title','product_type','vendor','price','quantity']]
    products.columns = ['ID','Name','Product Type','Vendor','Price','Quantity']
    # Data to be sent to the pdf template
    context = {
        "storeinfo":storeinfo,
        'title':'Products List Report',
        'user': request.user.username,
        'table': products.to_html(classes=['table', 'table-striped', 'bg-white', 'text-center'],index=False,escape=False),
    }
    # Export Filename
    filename = f"Products_List_Report_{strftime('%Y-%m-%d', localtime())}.pdf"
    # Activity Log
    add_activity(logged_user=request.user,activity_type='DOWNLOAD PDF',
                 activity_location='PRODUCT LIST',
                 activity_message=f"Products_List_Report_{strftime('%Y-%m-%d', localtime())}.pdf has been downloaded")
    # Generate PDF via render_to_pdf()
    return render_to_pdf(request,'reports/report.html', filename, context)
    

def export_graphs_pdf(request):
    if request.method == "GET":
            
        if request.GET.get('date-filter') == 'daily':
            
            time = 'week'
            
            # Get orders for this week
            one_week_ago = timezone.now() - timedelta(days=7)
            orders = Order.objects.filter(date_created__gte=one_week_ago).values('date_created','total')
            sales = pd.DataFrame(orders).set_index('date_created').groupby(pd.Grouper(freq='d')).sum(numeric_only=False)
            sales.index = sales.index.strftime('%b %d')
            
            # Get sum of sales last week
            prev_week = one_week_ago - timedelta(days=7)
            prev = Order.objects.filter(date_created__lte=one_week_ago)
            prev_sales = prev.filter(date_created__gte=prev_week).aggregate(Sum('total'))['total__sum']
            
            # Get Order Products this week
            products = OrderProduct.objects.filter(date__gte=one_week_ago).values('date','product_title','quantity','price')
            
            # Get Order Products last week
            prevs = OrderProduct.objects.filter(date__lte=one_week_ago).values('date','product_title','quantity','price')
            prev_products =  prevs.filter(date__gte=prev_week).values('date','product_title','quantity','price')
            
        elif request.GET.get('date-filter') == 'weekly':
            
            time = 'month'
            
            order_year = Order.objects.filter(date_created__year=timezone.now().year)
            
            # Get orders for this month
            orders = order_year.filter(date_created__month=timezone.now().month).values('date_created','total')
            sales = pd.DataFrame(orders).set_index('date_created').groupby(pd.Grouper(freq='W')).sum(numeric_only=False)
            sales.index = sales.index.strftime('%b %Y Week %V')
            
            # Get sum of sales last month
            prev_sales = order_year.filter(date_created__month=timezone.now().month-1).values('date_created','total').aggregate(Sum('total'))['total__sum']
            
            order_prod_year = OrderProduct.objects.filter(date__year=timezone.now().year)
            
            # Get Order Products this month
            products = order_prod_year.filter(date__month=timezone.now().month).values('date','product_title','quantity','price')
            
            # Get Order Products last month
            prev_products = order_prod_year.filter(date__month=timezone.now().month-1).values('date','product_title','quantity','price')
            
        elif request.GET.get('date-filter') == 'yearly':
            time = ''
            
            orders = Order.objects.all().values('date_created','total')
            sales = pd.DataFrame(orders).set_index('date_created').groupby(pd.Grouper(freq='Y')).sum(numeric_only=False)
            sales.index = sales.index.strftime('%Y')
            
            prev_sales = 0      
            products = OrderProduct.objects.all().values('date','product_title','quantity','price')   
            prev_products = []
        else:   
            # Get sales for this year
            time = 'year'
            orders = Order.objects.filter(date_created__year=timezone.now().year).values('date_created','total')
            sales = pd.DataFrame(orders).set_index('date_created').groupby(pd.Grouper(freq='M')).sum(numeric_only=False)
            sales.index = sales.index.strftime('%b %Y')
            
            # Get sum of sales last year
            prev_sales = Order.objects.filter(date_created__year=timezone.now().year-1).values('date_created','total').aggregate(Sum('total'))['total__sum']
            
            # Get Order Products this year
            products = OrderProduct.objects.filter(date__year=timezone.now().year).values('date','product_title','quantity','price')
            
            # Get Order Products last year
            prev_products = OrderProduct.objects.filter(date__year=timezone.now().year-1).values('date','product_title','quantity','price')
            
                    
    else:   
        # Default graph view - Sales of current year grouped by month
        time = 'year'
        orders = Order.objects.filter(date_created__year=timezone.now().year).values('date_created','total')
        sales = pd.DataFrame(orders).set_index('date_created').groupby(pd.Grouper(freq='M')).sum(numeric_only=False)
        sales.index = sales.index.strftime('%b %Y')
        
        # Get sum of sales last year
        prev_sales = Order.objects.filter(date_created__year=timezone.now().year-1).values('date_created','total').aggregate(Sum('total'))['total__sum']
        
        # Get Order Products this year
        products = OrderProduct.objects.filter(date__year=timezone.now().year).values('date','product_title','quantity','price')
        
        # Get Order Products last year
        prev_products = OrderProduct.objects.filter(date__year=timezone.now().year-1).values('date','product_title','quantity','price')
        
    # Get product ranks
    products_rank = pd.DataFrame(products).groupby(['product_title','price'],
                                                   as_index=False).sum('quantity').sort_values(by=['quantity'], ascending=False).head(10)
    total_sales = sales['total'].sum()
    
    # products_rank['product_title'] = [f'{product[:45]}' for product in products_rank['product_title']]
    products_rank['total'] = products_rank['price'] * products_rank['quantity']
    products_rank['percent'] =  products_rank['total'] / total_sales * 100
    
    prev_sales = prev_sales if prev_sales != None else 0
    sales_change = 100 if prev_sales == 0 else (total_sales - prev_sales) / prev_sales * 100
    
    products_sold = products.aggregate(Sum('quantity'))['quantity__sum']
    
    # return render(request, 'sales/graphs.html',context)
    
    # pos = np.arange(10)+ 2 

    # fig = plt.figure(figsize=(5, 3))
    # ax = fig.add_subplot(111)

    # ax.barh(pos, np.arange(1, 11), align='center')
    # ax.set_yticks(pos)
    # ax.set_yticklabels(('#hcsm',
    #     '#ukmedlibs',
    #     '#ImmunoChat',
    #     '#HCLDR',
    #     '#ICTD2015',
    #     '#hpmglobal',
    #     '#BRCA',
    #     '#BCSM',
    #     '#BTSM',
    #     '#OTalk',), 
    #     fontsize=15)
    # ax.set_xticks([])
    # ax.invert_yaxis()

    # ax.set_xlabel('Popularity')
    # ax.set_ylabel('Hashtags')
    # ax.set_title('Hashtags')

    # sf = sales.reset_index()
    # sf.plot(x="date_created", y="total", kind="bar")
    
    plt.plot(sales.index, sales['total'])
    plt.title('Total Sales')
    plt.xlabel('Months')
    plt.ylabel('Total Sales')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    products_rank['product_title'] = [f'{product[:15]}...' for product in products_rank['product_title']]
    new_df = products_rank[['product_title','total']]
    
    new_df['total'] = pd.to_numeric(new_df["total"], downcast="float")
    
    sns.barplot(data=new_df, x="product_title", y="total")
    plt.title('Product Sales')
    plt.xlabel('')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=10)

    plot_file = BytesIO()
    plt.savefig(plot_file,format='png')
    plot_file.seek(0)
    plot_png = plot_file.getvalue()
    plot_file.close()
    
    products_plot = base64.b64encode(plot_png)
    products_plot = products_plot.decode('utf-8')
    
    products_rank = json.loads(products_rank.reset_index().to_json(orient='records'))
                               
    context={
        'time':time,
        'total_sales':total_sales,
        'prev_sales':prev_sales,
        'sales_change':sales_change,
        'products_count':products_rank,
        'products_count_change':prev_products,
        'monthly_sales':sales,
        'order_count':orders.count(),
        'products_sold':products_sold,
        'quantity_change': 100 if prev_products.count() == 0 else (products_sold - prev_products.count()) / prev_products.count() * 100,
        'user':request.user.username,
        'sales':graphic,
        'products_plot':products_plot,
    }
    
    return render_to_pdf(request,'reports/report_analytics.html', f'analytics.pdf', context)
    # return render(request,'reports/report_analytics.html', context)


# ------------------excel export------------------------------------
@login_required
def exportproduct_excel(request):
    # Get Products
    if 'products' in request.session:
        products = request.session['products']
    else:
        endpoint = 'products.json?fields=id,title,product_type,vendor,tags,variants,images&status=active'
        df = pd.DataFrame(get_api_json(endpoint)['products'])
        df = df.set_index('id')
        # Set session variable to generate filtered reports
        df = df.reset_index().to_json(orient='records')
        products = json.loads(df)
        
    response= HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Inventory '+\
        str(strftime('%Y-%m-%d', localtime()))+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Inventory')
    style = xlwt.easyxf('align: horiz center; font: bold on;')
    ws.write(0,0,'Inventory Products',style)
    ws.merge(0,0,0,7)
    row_num = 1
    font_style=xlwt.XFStyle()
    font_style.font.bold=True

    columns=['ID','Name','Product Type','Vendor','Tags','Price','Quantity']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style=xlwt.XFStyle()
    
    
    rows=[]
    for product in products:
        rows.append((product['id'], product['title'], product['product_type'],product['vendor'],"".join(product['tags']),product['variants'][0]['price'],product['variants'][0]['inventory_quantity']))

    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)
    add_activity(logged_user=request.user,activity_type='DOWNLOAD',activity_location='PRODUCT LIST',activity_message=f"Product_List_Report_{strftime('%Y-%m-%d', localtime())}.xlt has been downloaded")
    return response

@login_required
def store_info(request):
    storeinfo = StoreInfo.objects.filter().first()
    notifications = Notifications.objects.filter(user=request.user)
    context = {
        'storeinfo':storeinfo,
        'label':'Settings',
        'notifications':notifications,
    }
    return render(request, 'reports/store_info.html', context)

@login_required
def store_info_change(request):
    storeinfo = StoreInfo.objects.first()
    notifications = Notifications.objects.filter(user=request.user)
    if request.method=="POST":
        storeinfo_form = StoreForm(request.POST,request.FILES,instance=storeinfo)
        if storeinfo_form.is_valid():
            storeinfo_form.save()
            name = request.user.username
            add_activity(logged_user=request.user,activity_type='CHANGE',activity_location='STORE',activity_message=f'Store has been updated.')
            messages.success(request,f"{name} your store has been successfully changed.")
            return redirect('store')
    else:
        storeinfo_form = StoreForm(instance=storeinfo)
    context = {
        'label':'Settings',
        'storeinfo_form':storeinfo_form,
        'notifications':notifications,
    }
    return render(request, 'reports/store_info_change.html', context)

@login_required
def view_settings(request):
    context = {'notifications':Notifications.objects.filter(user=request.user)}
    return render(request, 'reports/setting.html', context)


def delete_notification(request,pk):
    notif = Notifications.objects.get(id=pk)
    notif.delete()
    
    return redirect('dashboard-index')

def delete_all_notification(request):
    notif = Notifications.objects.filter(user=request.user)
    notif.delete()
    
    return redirect('dashboard-index')


def notif_view(request):
    notif = EmailNotification.objects.all().first()
    context = {
        'notif':notif,
        'notifications':Notifications.objects.filter(user=request.user)
    }
    return render(request, 'reports/notif.html', context)


def email_notify(request):
    user_list = []
    users = User.objects.all()
    for user in users:
        if user.is_staff:
            user_list.append(user.email)
    
    
    endpoint = 'products.json?limit=250&fields=id,title,variants&status=active'
    prod = get_api_json(endpoint)['products']
    
    df = pd.DataFrame(prod)
    df['quantity'] = [df.variants[x][0]['inventory_quantity'] for x in range(len(df))]
    df = df.drop(columns=['variants',])
    df = df.drop(df[df.quantity > 0].index).set_index('id').reset_index()
    df = df.drop(columns=['quantity',])
    df.columns = ['ID','OUT OF STOCK PRODUCTS']
    
    html_str = df.to_string()
    
    send_mail(
        subject='Out of Stock Products',
        message=html_str,
        from_email='one.time.sales.405@gmail.com',
        recipient_list=user_list,
        fail_silently=False,
    )
    return redirect('settings_view')

    
def notif_update(request):
    notif = EmailNotification.objects.all().first()
    if request.method == 'POST':
        freq = request.POST.get('frequency')
        if freq == 'Daily':
            sched = Schedule.DAILY
        elif freq == 'Weekly':
            sched = Schedule.WEEKLY
        else:
            sched = Schedule.MONTHLY
        
        time = request.POST.get('time')
        day = request.POST.get('day')
        
        datetimes = datetime.strptime(f'{day} {time}', '%Y-%m-%d %H:%M:%S')
        
        notif_form = NotificationForm(request.POST,instance=notif)
        notif_form.save()
        if request.POST.get('notification'):
            schedule('inventory.views.email_notify',
                schedule_type=sched,
                next_run=datetimes,repeats=-1)
            
        return redirect('notif-view')

    context = {
        'notif':notif,
        'form':NotificationForm(instance=notif),
        'notifications':Notifications.objects.filter(user=request.user)
    }
    return render(request, 'reports/notif_info_change.html', context)
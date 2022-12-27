from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sales.models import Order, OrderProduct
from django.db.models import Sum
from django.utils import timezone
from reports.models import Notifications
import pandas as pd, json

# Create your views here.
@login_required
def index(request):
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
    products_rank = json.loads(products_rank.reset_index().to_json(orient='records'))
    
    prev_sales = prev_sales if prev_sales != None else 0
    sales_change = 100 if prev_sales == 0 else (total_sales - prev_sales) / prev_sales * 100
    
    # Notifications
    notifications = Notifications.objects.filter(user=request.user)
    
    products_sold = products.aggregate(Sum('quantity'))['quantity__sum']
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
        'quantity_change': 100 if prev_products.count() == 0 else (products.count() - prev_products.count()) / prev_products.count() * 100,
        'state':'dashboard',
        'notifications':notifications,
    }
    return render(request, 'dashboard/index1.html', context)
    
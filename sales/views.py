from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from .models import *
from .forms import CustomerForm
from datetime import timedelta
from facmasys.utils import get_api_json, post_api_json, to_peso, add_activity, ExportPDF, HTTPResponseHXRedirect
import json, pandas as pd, numpy as np
from time import strftime, localtime
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django_tables2.export.views import ExportMixin
from .tables import *
from .filters import *
from django.http import HttpResponse
from reports.models import Notifications


products = []
def refresh_products():
    endpoint = 'products.json?limit=250&fields=id,title,product_type,vendor,tags,variants,images&status=active'
    prod = get_api_json(endpoint)['products']
    df = pd.DataFrame(prod)
    df['price'] = [df.variants[x][0]['price'] for x in range(len(df))]
    df['quantity'] = [df.variants[x][0]['inventory_quantity'] for x in range(len(df))]
    df = df.drop(columns=['variants',])
    df['images'] = [df.images[x][0]['src'] for x in range(len(df))]
    df = df.drop(df[df.quantity <= 0].index).set_index('id').reset_index().to_json(orient='records')
    global products
    products = json.loads(df)


# Create your views here.
class SalesView(LoginRequiredMixin, SingleTableMixin, ExportMixin, ExportPDF, FilterView):
    table_class = SalesTable
    filterset_class = SalesFilter
    queryset = Order.objects.values('id','invoice_number','date_created','staff__username','customer__name',
                                    'subtotal','vat','total','pay_method','pay_id','status').filter(status='Completed')
    paginate_by = 10
    state = 'sales'
    label = 'Sales'
    sales_active = 'completed'
    export_formats = ('xlsx','csv','pdf')
    exclude_columns = ('id',)
    export_name = f"Sales_List_Report_{strftime('%Y-%m-%d', localtime())}"
    dataset_kwargs = {"title": "Sales"}
    
    def get_context_data(self, *args, **kwargs):
        context = super(SalesView, self).get_context_data(*args, **kwargs)
        context['notifications'] = Notifications.objects.filter(user=self.request.user)
        return context
    
    def get_template_names(self):

        return 'partials/table.html' if self.request.htmx else 'sales/sales.html'
    
    
class SalesReturnedView(SalesView):
    queryset = Order.objects.values('id','invoice_number','date_created','staff__username','customer__name',
                                    'subtotal','vat','total','pay_method','pay_id','status').filter(status='Returned')
    sales_active = 'returned'


@login_required
def sales_return(request, pk):
    item = Order.objects.get(id=pk)
    item.status = "Returned"
    item.save()
    
    # products = item.products.all()
    # services = item.services.all()
    
    # # Archive all products related to order
    # for product in products:
    #     OrderProductArchive.objects.create(id=product.id,date=product.date,item_id=product.item_id,
    #                                        product_title=product.product_title,quantity=product.quantity,
    #                                        price=product.price,cost=product.cost) 
    # products.delete()
        
    # # Archive all services related to order
    # for service in services:
    #     OrderServiceArchive.objects.create(id=service.id,date=service.date,service=service.service,labor=service.labor)
    # services.delete()

    messages.success(request,f'Order with Invoice No: {item.invoice_number} has been marked as returned.')
    return redirect('sales')


@login_required
def get_values(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        Cart.objects.create(user=request.user)
    cart = Cart.objects.get(user=request.user)
    cart_products = cart.products.all()
    cart_services = cart.service.all()
    values = update_cart(cart)
            
    context = {
        'form': CustomerForm(),
        'cart':cart,
        'cart_products':cart_products,
        'cart_services':cart_services,
    }
    context |= values
    
    return context


@login_required
def update_cart(cart):
    return {'subtotal':f'{cart.subtotal:.2f}','vat':cart.vat,'total':cart.total,'button':'disabled' if float(cart.total) <= float(0) else ''}


@login_required
def add_order(request):
    values = get_values(request)               
    cart_products = values['cart_products']     
    cart_services = values['cart_services']
    customer = None
    
    # HttpResponse for Error Message
    error_html = '<div id="err-text" class="alert alert-danger my-2" role="alert">'
    
    if request.method == 'POST':
        
        if request.POST.get('cust').strip() == '' and request.POST.get('cust_name').strip() == '':
            return HttpResponse(f'{error_html}Customer details are required.</div>')
        
        elif request.POST.get('cust').strip() != '':
            
            if Customer.objects.filter(email=request.POST['cust']).exists():
                customer = Customer.objects.get(email=request.POST.get('cust'))
            elif Customer.objects.filter(contact=request.POST['cust']).exists():
                customer = Customer.objects.get(contact=request.POST.get('cust'))
            else:
                return HttpResponse(f'{error_html}Customer email or contact number does not match any of our records.</div>')
        else:
            
            if request.POST.get('cust_name').strip() == '':
                return HttpResponse(f'{error_html}Customer details are required.</div>')
            elif request.POST.get('email').strip() == '':
                return HttpResponse(f'{error_html}New Customer email is required.</div>')
            elif request.POST.get('contact').strip() == '':
                return HttpResponse(f'{error_html}New Customer contact number is required.</div>')
            elif Customer.objects.filter(email=request.POST.get('email')).exists():
                return HttpResponse(f'{error_html}Email is already registered.</div>')
            elif Customer.objects.filter(contact=request.POST.get('contact')).exists():
                return HttpResponse(f'{error_html}Contact number is already registered.</div>')
            
            try:
                int(request.POST.get('contact'))
                if len(request.POST.get('contact')) < 10:
                    return HttpResponse(f'{error_html}Contact number is not valid.</div>')
            except ValueError:
                return HttpResponse(f'{error_html}Contact number is not valid.</div>')
        
        # Check for payment reference number for payment methods other than cash
        if request.POST.get('pay-method') != 'Cash':
            if request.POST.get('pay-id').strip() == '':
                return HttpResponse(f'{error_html}Payment Reference Number is required for payment methods other than cash.</div>')
        
        #Set Invoice number
        if Order.objects.all().count() > 0:
            # df = pd.DataFrame(Order.objects.all())
            # print(df)
            invoice = int(Order.objects.all().first().invoice_number) + int(1)
        else:
            invoice = 1
            
        # Create new customer 
        if customer == None:
            customer = Customer.objects.create(name=request.POST.get('cust_name'),email=request.POST.get('email'),
                                    contact=request.POST.get('contact'),address=request.POST.get('address'),
                                    car_make=request.POST.get('car'),plate_no=request.POST.get('plate-no'))
            customer.save()
        
        # Create Order
        order = Order.objects.create(invoice_number=invoice, staff=request.user, 
                                        customer=customer, 
                                        vat=values['vat'], subtotal=values['cart'].subtotal, total=values['cart'].total, 
                                        pay_method=request.POST.get('pay-method'), pay_id=request.POST.get('pay-id'), status="Completed")
        
        # Add products in cart to order
        for cproduct in cart_products:
            print(cproduct.item_id)
            # Get inventory item id from product variant
            endpoint = f'products/{str(cproduct.item_id)}/variants.json'
            inventory_item_id = get_api_json(endpoint)['variants'][0]['inventory_item_id']     
            
            # Get cost from Inventory Item
            endpoint = f'inventory_items/{str(inventory_item_id)}.json'
            cost = get_api_json(endpoint)['inventory_item']['cost']     
            
            # Create an Order Product record and link it to Order
            order.products.add(OrderProduct.objects.create(item_id=str(cproduct.item_id), product_title=cproduct.product_title, 
                                                        quantity=cproduct.quantity, price=cproduct.price, cost=cost))
            
            # Get Store Location ID
            location_id = get_api_json('locations.json')['locations'][0]['id']      
            
            # Update product quantity from inventory
            inventory_level_payload = {
                "location_id":int(location_id),
                "inventory_item_id":int(inventory_item_id),
                "available_adjustment":int(-cproduct.quantity),
            }
            endpoint = 'inventory_levels/adjust.json'
            post_api_json(endpoint,inventory_level_payload)    
        
        cart_products.delete()
            
        # Add services in cart to order
        for cservice in cart_services:
            order.services.add(OrderService.objects.create(service=cservice.service, labor=cservice.labor))
        cart_services.delete()
                    
        # Activity Log
        add_activity(logged_user=request.user,activity_type='ADD',activity_location='ORDER',
                        activity_message=f"Order with Invoice Number ({invoice}) has been successfully created for {request.POST['cust']}.")
                
        # Display Invoice
        customer = Order.objects.get(invoice_number=invoice)
        return HTTPResponseHXRedirect(redirect_to=reverse_lazy("sales-customer-detail", kwargs={'pk': customer.id }))
        

@login_required
def order(request):
    refresh_products()
    product_page = Paginator(products,10)
    product_page_list = request.GET.get('product_page') if request.GET.get('product_page') else 1
    product_page = product_page.get_page(product_page_list)
    
    services = Service.objects.all().order_by('id')
    service_page = Paginator(services,10)
    service_page_list = request.GET.get('service_page') if request.GET.get('service_page') else 1
    service_page = service_page.get_page(service_page_list)
    
    display = 'products'
    if request.GET.get('service_page'):
        display = 'services'
        
    context = {
        'form': CustomerForm(),
        'products':product_page,
        'services':service_page,
        'display':display,
        'product_count':product_page.paginator.count,
        'product_itemcount':product_page.paginator.count if product_page.paginator.per_page * product_page.number > product_page.paginator.count else product_page.paginator.per_page * product_page.number,
        'service_count':service_page.paginator.count,
        'service_itemcount':service_page.paginator.count if service_page.paginator.per_page * service_page.number > service_page.paginator.count else service_page.paginator.per_page * service_page.number,
        'types':{product['product_type'] for product in products},
        'brands':{product['vendor'] for product in products},
        'service_categories':Service.objects.values('category').distinct(),
        'state':'order',
        'notifications':Notifications.objects.filter(user=request.user)
    }
    context |= get_values(request)
    
    return render(request, 'sales/order.html', context)


def get_product(pk):
    endpoint = 'products/' + str(pk) + '.json'
    return get_api_json(endpoint)['product']


def get_quantity(item_id):
    endpoint = f'inventory_levels.json?inventory_item_ids={item_id}'
    return int(get_api_json(endpoint)['inventory_levels'][0]['available'])      # Get product quantity


def add_cart_product(request, pk):
    values = get_values(request) 
    product = get_product(pk)   # Get Product
    if values['cart_products'].filter(item_id=pk).exists():
        cart_product = values['cart_products'].get(item_id=pk)
        max_quantity = get_quantity(product['variants'][0]['inventory_item_id'])
        if request.method == 'GET':
            qty = request.GET[f'quantity{cart_product.item_id}']
            
            if qty == '':
                cart_product.quantity = 1
                messages.warning(request,f"Quantity is required. Updated {product['title']} quantity to 1.")
            elif int(qty) > max_quantity:
                cart_product.quantity = max_quantity
                messages.warning(request,f"Cart quantity exceeded product quantity. Updated {product['title']} quantity to {max_quantity}.")
            elif int(qty) < 1:
                 cart_product.quantity = 1
                 messages.warning(request,f"Quantity must be greater than 0. Updated {product['title']} quantity to 1.")
            else:
                cart_product.quantity = int(qty)
                messages.success(request,f"{product['title']} quantity has been updated. (Updated Quantity: {qty})")
        else:
            if cart_product.quantity != max_quantity:
                cart_product.quantity += 1
                messages.warning(request,f"{product['title']} is already in cart. 1 Quantity has been added instead.")
            else:
                messages.warning(request,f"{product['title']} is already in cart and has reached it's maximum quantity.")
        cart_product.save()
    else:
        values['cart'].products.add(CartProduct.objects.create(item_id=product['id'],product_title=product['title'],quantity=1,price=float(product['variants'][0]['price'])))
        messages.success(request,f"{product['title']} has been added to cart.")
        
    values |= update_cart(values['cart'])
    return render(request, 'sales/cart.html', values)

@login_required
def add_cart_service(request, pk):
    values = get_values(request)
    service = Service.objects.get(id=pk)
            
    if not values['cart_services'].filter(service=service).exists():           
        values['cart'].service.add(CartService.objects.create(service=service,labor=service.labor))
        messages.success(request,f"{service.name} has been added to cart.")
    elif request.method == 'POST':
        cart_service = values['cart_services'].get(service=service)
        cart_service.labor = cart_service.service.labor
        cart_service.save()
        messages.warning(request,f"{service.name} is already in cart. Labor has been set back to {to_peso(cart_service.service.labor)} instead.")
    if request.method == 'GET':
        cart_service = values['cart_services'].get(service=service)
        nlabor = request.GET[f'labor{cart_service.id}']
        if nlabor == '' or float(nlabor) < 1.00:   
            cart_service.labor = cart_service.service.labor
            messages.warning(request,f"Labor must be greater than ({to_peso(1.00)}). {service.name} labor has been set back to {to_peso(cart_service.service.labor)}")
        else:
            cart_service.labor = nlabor
            messages.success(request,f"{service.name} labor has been updated. (Updated Labor: {to_peso(nlabor)})")
        cart_service.save()
    
    values |= update_cart(values['cart'])
    return render(request, 'sales/cart.html', values)

@login_required
def delete_cart_product(request, pk):
    values = get_values(request)
    product = values['cart'].products.get(item_id=pk)
    messages.warning(request,f"{product.product_title} was removed from cart.")
    product.delete()
    values |= update_cart(values['cart'])
    return render(request, 'sales/cart.html', values)

@login_required
def delete_cart_service(request, pk):
    values = get_values(request)
    service = values['cart'].service.get(service=Service.objects.get(id=pk))
    messages.warning(request,f"{service.service.name} was removed from cart.")
    service.delete()
    values |= update_cart(values['cart'])
    return render(request, 'sales/cart.html', values)


@login_required
@require_http_methods(["GET"])
def order_product_search(request):
    df = pd.DataFrame(products)
    if request.GET['type-filter'] != 'all':
        df = df[df.product_type.str.contains(request.GET['type-filter'])]
    if request.GET['vendor-filter'] != 'all':
        df = df[df.vendor.str.contains(request.GET['vendor-filter'])]
    q = request.GET['q']
    if q != '':
        df['id'] = df['id'].apply(str)
        df['tags'] = df['tags'].apply(str)
        df = df[(df.id.str.contains(q,case=False)) | (df.title.str.contains(q,case=False)) | (df.tags.str.contains(q,case=False))]
    
    df = df.set_index('id')
    df = df.reset_index().to_json(orient='records')
    items = json.loads(df)
    product_page = Paginator(items,10)
    product_page_list = request.GET.get('product_page') if request.GET.get('product_page') else 1
    product_page = product_page.get_page(product_page_list)
    display = 'products'
    context = {
        'notifications':Notifications.objects.filter(user=request.user),
        'display':display,
        'products':product_page,
        'product_count':product_page.paginator.count,
        'product_itemcount':product_page.paginator.count if product_page.paginator.per_page * product_page.number > product_page.paginator.count else product_page.paginator.per_page * product_page.number,
    }
    return render(request, 'sales/product_list.html', context)

@login_required
@require_http_methods(["GET"])
def order_service_search(request):
    services = Service.objects.all()
    services = services.filter(name__icontains=request.GET['name'])
    if request.GET['category-filter'] != 'all':
        services = services.filter(category__exact=request.GET['category-filter'])
    service_page = Paginator(services,10)
    service_page_list = request.GET.get('service_page') if request.GET.get('service_page') else 1
    service_page = service_page.get_page(service_page_list)
    display = 'services'
    context = {
        'display':display,
        'notifications':Notifications.objects.filter(user=request.user),
        'services':service_page,
        'service_count':service_page.paginator.count,
        'service_itemcount':service_page.paginator.count if service_page.paginator.per_page * service_page.number > service_page.paginator.count else service_page.paginator.per_page * service_page.number,
    }
    return render(request, 'sales/service_list.html', context)


@login_required
def customer_detail(request, pk):
    customer = Order.objects.get(id=pk)
    context = {
        'customer':customer,
        'notifications':Notifications.objects.filter(user=request.user)
    }
    return render(request, 'sales/customer_detail.html', context)


#analytics----------------------------------------------------------------------
@login_required
def analytics(request):
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
    
    products_rank['product_title'] = [f'{product[:40]}' for product in products_rank['product_title']]
    products_rank['total'] = products_rank['price'] * products_rank['quantity']
    products_rank['percent'] =  products_rank['total'] / total_sales * 100
    products_rank = json.loads(products_rank.reset_index().to_json(orient='records'))
    
    prev_sales = prev_sales if prev_sales != None else 0
    sales_change = 100 if prev_sales == 0 else (total_sales - prev_sales) / prev_sales * 100
    
    products_sold = products.aggregate(Sum('quantity'))['quantity__sum']
    context={
        'label':'Analytics',
        'state':'analytics',
        'time':time,
        'total_sales':total_sales,
        'prev_sales':prev_sales,
        'sales_change':sales_change,
        'products_count':products_rank,
        'products_count_change':prev_products,
        'monthly_sales':sales,
        'order_count':orders.count(),
        'products_sold':products_sold,
        'notifications':Notifications.objects.filter(user=request.user),
        'quantity_change': 100 if prev_products.count() == 0 else (products.count() - prev_products.count()) / prev_products.count() * 100,
    }
    return render(request, 'sales/analytics.html',context)


@login_required
def graphs(request):
    if request.method == "GET":
            
        if request.GET['date-filter'] == 'daily':
            
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
            
        elif request.GET['date-filter'] == 'weekly':
            
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
            
        elif request.GET['date-filter'] == 'yearly':
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
    
    products_rank['product_title'] = [f'{product[:40]}' for product in products_rank['product_title']]
    products_rank['total'] = products_rank['price'] * products_rank['quantity']
    products_rank['percent'] =  products_rank['total'] / total_sales * 100
    products_rank = json.loads(products_rank.reset_index().to_json(orient='records'))
    
    prev_sales = prev_sales if prev_sales != None else 0
    sales_change = 100 if prev_sales == 0 else (total_sales - prev_sales) / prev_sales * 100
    
    products_sold = products.aggregate(Sum('quantity'))['quantity__sum']
    context={
        'label':'Analytics',
        'time':time,
        'total_sales':total_sales,
        'prev_sales':prev_sales,
        'sales_change':sales_change,
        'products_count':products_rank,
        'products_count_change':prev_products,
        'monthly_sales':sales,
        'order_count':orders.count(),
        'products_sold':products_sold,
        'notifications':Notifications.objects.filter(user=request.user),
        'quantity_change': 100 if prev_products.count() == 0 else (products_sold - prev_products.count()) / prev_products.count() * 100,
    }
    return render(request, 'sales/graphs.html',context)

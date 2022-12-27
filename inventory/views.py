from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django_filters.views import FilterView
from .models import *
from reports.models import Notifications
from .forms import *
from .filters import *
from .tables import *
from django_tables2 import SingleTableMixin
from django_tables2.export.views import ExportMixin
from time import strftime, localtime
from speedlabproject.utils import add_activity, get_api_json, post_api_json, put_api_json, ExportPDF
from django.core.mail import send_mail
import json, base64, pandas as pd


# PRODUCTS -----------------------------------------------------------------------------------
products, state = [], 'all'

def refresh_products():
    global products, state
    state = 'all'
    endpoint = "products.json?limit=250&fields=id,title,product_type,vendor,tags,variants,images&status=active"
    prod = get_api_json(endpoint)['products']
    df = pd.DataFrame(prod)
    df['price'] = [df.variants[x][0]['price'] for x in range(len(df))]
    df['quantity'] = [df.variants[x][0]['inventory_quantity'] for x in range(len(df))]
    df = df.drop(columns=['variants',])
    df['images'] = [df.images[x][0]['src'] for x in range(len(df))]
    df = df.set_index('id').reset_index().to_json(orient='records')
    
    products = json.loads(df)
    
    
@login_required
def product(request):
    if state == 'all':
        refresh_products()
        if 'products' in request.session:
            del request.session['products']
            request.session.modified = True
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)   
        
        images = []
        if request.FILES.getlist('image'):
            for img in request.FILES.getlist('image'):
                images.append({"attachment":str(base64.b64encode(img.read()))[1:]})
        else:
            with open(str(settings.MEDIA_ROOT) + '/product.png', 'rb') as image_file:
                images.append({"attachment":str(base64.b64encode(image_file.read()))[1:]})

        # Add product to shopify via REST API
        endpoint = 'products.json'
        payload = {
            "product": {
                "title":form["title"].value(),
                "body_html":form["description"].value(),
                "vendor":form["vendor"].value(),
                "product_type":form["product_type"].value(),
                "tags":form["tags"].value().replace(", ",",").split(","),
                "inventory_management":"shopify",
                "variants":[{
                    "option1":"Default Title",
                    "price":form["price"].value(),
                    "sku":form["sku"].value() if form["sku"].value().strip() != '' else 'N/A'
                }],
                "images":images
            }
        }
        post_resp = post_api_json(endpoint,payload)
        
        # Update Inventory Item
        inventory_item_id = post_resp['product']['variants'][0]['inventory_item_id']
        inventory_item_payload = {
            "inventory_item": {
                "id": inventory_item_id,
                "tracked":True,
            }
        }
        endpoint = 'inventory_items/' + str(inventory_item_id) + '.json'
        print('PUT: ',put_api_json(endpoint,inventory_item_payload))
        
        # Update Low Stock Limit
        endpoint = f"products/{post_resp['product']['id']}/metafields.json"
        payload = {"metafield":{"namespace":"custom","key":"low_stock","value":form["low_stock"].value(),"type":"number_integer"}}
        print('POST: ',post_api_json(endpoint,payload))
        
        messages.success(request, f"{ form['title'].value() } has been added.")
        add_activity(logged_user=request.user,activity_type='ADD',activity_location='PRODUCT',activity_message=f"{ form['title'].value() } has been added.")
        
    else:
        form = ProductForm()
        
    page = Paginator(products,10)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    
    # Notifications
    notifications = Notifications.objects.filter(user=request.user)
    
    context = {
        'page':page,
        'form':form,
        'types':{product['product_type'] for product in products},
        'brands':{product['vendor'] for product in products},
        'count':page.paginator.count if page.paginator.per_page * page.number > page.paginator.count else page.paginator.per_page * page.number,
        'itemcount':page.paginator.count,
        'state':'inventory',
        'label':'Product',
        'inventorypage_active':'product',
        'inventorystatus_active':state,
        'notifications':notifications,
    }
    return render(request, 'inventory/product.html', context)


def product_all(request):
    global state
    state = 'all'

    return redirect('inventory-product')
    

def product_active(request):
    global products, state
    state = 'active'
    endpoint = 'products.json?limit=250&fields=id,title,product_type,vendor,tags,variants,images&status=active'
    prod = get_api_json(endpoint)['products']
    
    df = pd.DataFrame(prod)
    df['price'] = [df.variants[x][0]['price'] for x in range(len(df))]
    df['quantity'] = [df.variants[x][0]['inventory_quantity'] for x in range(len(df))]
    df = df.drop(columns=['variants',])
    df['images'] = [df.images[x][0]['src'] for x in range(len(df))]
    df = df.drop(df[df.quantity <= 0].index).set_index('id').reset_index().to_json(orient='records')
    
    products = json.loads(df)
        
    # Set session variable to generate filtered reports
    request.session['products'] = products
    
    return redirect('inventory-product')


def product_out(request):
    global products, state
    state = 'out'
    endpoint = 'products.json?limit=250&fields=id,title,product_type,vendor,tags,variants,images&status=active'
    prod = get_api_json(endpoint)['products']
    
    df = pd.DataFrame(prod)
    df['price'] = [df.variants[x][0]['price'] for x in range(len(df))]
    df['quantity'] = [df.variants[x][0]['inventory_quantity'] for x in range(len(df))]
    df = df.drop(columns=['variants',])
    df['images'] = [df.images[x][0]['src'] for x in range(len(df))]
    df = df.drop(df[df.quantity > 0].index).set_index('id').reset_index().to_json(orient='records')
    
    products = json.loads(df)
    
    # Set session variable to generate filtered reports
    request.session['products'] = products
    
    return redirect('inventory-product')


def product_archived(request):
    global products, state
    state = 'archived'
    endpoint = 'products.json?limit=250&fields=id,title,product_type,vendor,tags,variants,images&status=archived'
    prod = get_api_json(endpoint)['products']
    
    df = pd.DataFrame(prod)
    df['price'] = [df.variants[x][0]['price'] for x in range(len(df))]
    df['quantity'] = [df.variants[x][0]['inventory_quantity'] for x in range(len(df))]
    df = df.drop(columns=['variants',])
    df['images'] = [df.images[x][0]['src'] for x in range(len(df))]
    df = df.set_index('id').reset_index().to_json(orient='records')
    
    products = json.loads(df)
    
    # Set session variable to generate filtered reports
    request.session['products'] = products
    
    return redirect('inventory-product')
    

@require_http_methods(["GET"])
def product_search(request): 
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
    # Set session variable to generate filtered reports
    df = df.reset_index().to_json(orient='records')
    
    items = json.loads(df)
    
    request.session['products'] = items
    
    page = Paginator(items,10)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    
    context = {
        'page':page,
        'count':page.paginator.count if page.paginator.per_page * page.number > page.paginator.count else page.paginator.per_page * page.number,
        'itemcount':page.paginator.count,
    }
    return render(request, 'inventory/product_list.html', context)
    

@login_required
def product_view(request,pk):
    endpoint = f'products/{str(pk)}.json'
    product = get_api_json(endpoint)['product']
    page = Paginator(products,10)
    page = page.get_page(1)
    
    # Notifications
    notifications = Notifications.objects.filter(user=request.user)
    
    context = {
        'form':ProductForm(),
        'product':product,
        'page':page,
        'product_view':True,
        'count':page.paginator.count if page.paginator.per_page * page.number > page.paginator.count else page.paginator.per_page * page.number,
        'itemcount':page.paginator.count,
        'state':'inventory',
        'label':'Product',
        'notifications':notifications,
    }
    return render(request, 'inventory/product.html', context)


@login_required
def product_archive(request,pk):
    endpoint = 'products/' + str(pk) + '.json'
    payload = {"product": {"id":pk,"status":"archived"}}
    response = put_api_json(endpoint,payload)
    messages.success(request,f"{response['product']['title']} has been successfully archived.")
    add_activity(logged_user=request.user,activity_type='ARCHIVE',activity_location='PRODUCT',activity_message=f"{response['product']['title']} has been successfully archived.")
    
    return redirect('inventory-product-archived')


@login_required
def product_restore(request,pk):
    endpoint = 'products/' + str(pk) + '.json'
    payload = {"product": {"id":pk,"status":"active"}}
    response = put_api_json(endpoint,payload)
    messages.success(request,f"{response['product']['title']} has been successfully restored.")
    add_activity(logged_user=request.user,activity_type='RESTORE',activity_location='PRODUCT',activity_message=f"{response['product']['title']} has been successfully restored.")
    
    return redirect('inventory-product-active')


@login_required
def product_update(request,pk):
    endpoint = 'products/' + str(pk) + '.json'
    product = get_api_json(endpoint)['product']
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        media = request.FILES.getlist('image')
        images = []
        for img in media:
            images.append({"attachment":str(base64.b64encode(img.read()))[1:]})
        
        # Update Product
        payload = {
            "product": {
                "id":pk
            }
        }
        if form["title"].value() != product['title'] and form["title"].value() != '':
            payload['product']['title'] = form["title"].value() 
        if form["description"].value().replace('\r','') != product['body_html'].replace('\r',''):
            payload['product']['body_html'] = form["description"].value()
        if form["vendor"].value() != product['vendor'] and form["vendor"].value() != '':
            payload['product']['vendor'] = form["vendor"].value()
        if form["product_type"].value() != product['product_type']:
            payload['product']['product_type'] = form["product_type"].value()
        if form["tags"].value().replace(", ",",") != "".join(product['tags']).replace(", ",","):
            payload['product']['tags'] = form["tags"].value().replace(", ",",").split(",")
        if len(images) > 0:
            for image in product['images']:
                images.append({"id":image['id']})
            payload['product']['images'] = images
            
        if len(payload['product']) > 1:
            print('PUT: ',put_api_json(endpoint,payload))
            
        # Update Product Variant
        if form["price"].value() != product['variants'][0]['price'] or form["sku"].value() != product['variants'][0]['sku'] and form["sku"].value() != '':
            variant_id = product['variants'][0]['id']
            payload2 = {"variant":{"id":variant_id}}
            if form["price"].value() != product['variants'][0]['price']:
                payload2['variant']['price'] = form["price"].value()
            if form["sku"].value() != product['variants'][0]['sku'] and form["sku"].value() != '':
                payload2['variant']['sku'] = form["sku"].value()
            
            if len(payload2['variant']) > 1:
                endpoint2 = 'variants/' + str(variant_id) + '.json'
                print('PUT: ',put_api_json(endpoint2,payload2))
        
        messages.success(request, f"{ form['title'].value() } has been updated.")
        add_activity(logged_user=request.user,activity_type='UPDATE',activity_location='PRODUCT',activity_message=f"{ form['title'].value() } has been updated.")
        return redirect('inventory-product')
    else:
        form = ProductForm(initial={
            'title':product['title'],'description':product['body_html'],'vendor':product['vendor'],'product_type':product['product_type'],
            'tags':"".join(product['tags']),'price':product['variants'][0]['price'],'sku':product['variants'][0]['sku']
            })
    page = Paginator(products,10)
    page = page.get_page(1)
    
    context = {
        'product':product,
        'page':page,
        'form':form,
        'product_update':True,
        'count':page.paginator.count if page.paginator.per_page * page.number > page.paginator.count else page.paginator.per_page * page.number,
        'itemcount':page.paginator.count,
        'state':'inventory',
        'label':'Product'
    }
    return render(request, 'inventory/product.html', context)


@login_required
def add_stock(request, pk):
    if request.method == 'POST':
        if int(request.POST['quantity']) > 0:
            try:
                assert float(request.POST['fees']) >= 0.00, 'Fees must be greater than or equal to zero.'
                # Get product
                endpoint = 'products/' + str(pk) + '.json'
                product = get_api_json(endpoint)['product']
                inventory_item_id = product['variants'][0]['inventory_item_id']
                inventory_item_payload = {
                    "inventory_item": {
                        "id": inventory_item_id,
                        "tracked":True,
                    }
                }
                if float(request.POST['base_price']) >= 0.00:
                    inventory_item_payload['inventory_item']['cost'] = request.POST['base_price']
                # Add Entry to Stock History
                addstockform = AddStockForm(request.POST)
                prod = addstockform.save(commit=False)
                if addstockform.is_valid():    
                    prod.product = product['title']
                    prod.gross_amount = round(float(request.POST['base_price']) * float(request.POST['quantity']) + float(request.POST['fees']),2)
                    prod.save()    
                # Update Inventory Item
                endpoint = 'inventory_items/' + str(inventory_item_id) + '.json'
                print('PUT: ',put_api_json(endpoint,inventory_item_payload))    
                # Get Store Location ID
                endpoint = 'locations.json'
                location_id = get_api_json(endpoint)['locations'][0]['id']
                # Update Inventory Level Quantity
                endpoint = 'inventory_levels/adjust.json'
                inventory_level_payload = {
                    "location_id":int(location_id),
                    "inventory_item_id":int(inventory_item_id),
                    "available_adjustment":int(request.POST['quantity']),
                }
                print('POST: ',post_api_json(endpoint,inventory_level_payload))  
                messages.success(request, 
                    f"{request.POST['quantity']} stock/s of {product['title']} has been added from {Supplier.objects.get(id=request.POST['supplier']).name}")
                # Activity Log
                add_activity(logged_user=request.user,activity_type='ADD',activity_location='STOCK',
                    activity_message=
                    f"{request.POST['quantity']} stock/s of {product['title']} has been added from {Supplier.objects.get(id=request.POST['supplier']).name}")
                return redirect('inventory-shipment')      
        # Check if price and quantity is valid.
            except ValueError:
                messages.error(request, 'Base Price must be greater than or equal to zero.')
            except AssertionError as msg:
                messages.error(request, msg)
            # return redirect('inventory-product')
        # else:
        messages.error(request, 'Quantity must be greater than 0')
        return redirect('inventory-product')
    # Display Products Paginated
    
    page = Paginator(products,10)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {
        'page':page,
        'add_stock':True,
        'form':ProductForm(),
        'add_stock_form':AddStockForm(),
        'count':page.paginator.count if page.paginator.per_page * page.number > page.paginator.count else page.paginator.per_page * page.number,
        'itemcount':page.paginator.count,
        'state':'inventory',    # Navbar state
        'label':'Product'
    }
    return render(request, 'inventory/product.html', context)


# SERVICE -----------------------------------------------------------------------------------
class ServiceView(LoginRequiredMixin, SingleTableMixin, CreateView, ExportMixin, ExportPDF, FilterView):
    table_class = ServiceTable
    filterset_class = ServiceFilter
    form_class = ServiceForm
    queryset = Service.objects.values()
    paginate_by = 10
    state = 'inventory'
    inventorypage_active = 'service'
    label = 'Service'
    inventorystatus_active ='active'
    export_formats = ('xlsx','pdf')
    exclude_columns = ('id',)
    export_name = f"Service_List_Report_{strftime('%Y-%m-%d', localtime())}"
    dataset_kwargs = {"title": "Service"}
        
    def get_template_names(self):

        return 'partials/table.html' if self.request.htmx else 'inventory/service.html'
    
    def form_valid(self, form):
        messages.success(self.request, 
                         f'Service {self.request.POST.get("name")} has been created.')
        add_activity(logged_user=self.request.user,activity_type='ADD',activity_location='SERVICE',
                     activity_message=f'{self.request.POST.get("name")} has been added.')
        form.save()
        
        return redirect('inventory-service')



class ServiceArchiveView(ServiceView):
    table_class = ServiceArchiveTable
    filterset_class = ServiceArchiveFilter
    queryset = ServiceArchive.objects.values()
    label = 'Service Archive'
    inventorystatus_active ='archive'
    export_name = f"Service_Archive_List_Report_{strftime('%Y-%m-%d', localtime())}"
    dataset_kwargs = {"title": "Service Archive"}

    def get_template_names(self):
    
        return 'partials/table.html' if self.request.htmx else 'inventory/service_archived.html'


class ServiceUpdateView(LoginRequiredMixin, SingleTableMixin, UpdateView):
    table_class = ServiceTable
    form_class = ServiceForm
    queryset = Service.objects.all()
    paginate_by = 10
    state = 'inventory'
    label = 'Service'
    modal = 'update'
    template_name = 'inventory/service.html'
        
    def form_valid(self, form):
        messages.success(self.request, 
                         f'Service {self.request.POST.get("name")} has been updated.')
        add_activity(logged_user=self.request.user,activity_type='UPDATE',activity_location='SERVICE',
                     activity_message=f'{self.request.POST.get("name")} has been updated.')
        form.save()
        
        return redirect('inventory-service')


@login_required
def service_archive(request,pk):
    service = Service.objects.get(id=pk)
    archive = ServiceArchive.objects.create(id=pk,name=service.name,category=service.category,
                                             labor=service.labor,image=service.image,
                                             remarks=service.remarks)
    archive.save()
    messages.success(request,f"{service.name} has been successfully archived.")
    add_activity(logged_user=request.user,activity_type='ARCHIVE',activity_location='SERVICE',activity_message=f"{service.name} has been successfully archived.")
    service.delete()
    
    return redirect('inventory-service-archived')


@login_required
def service_restore(request,pk):
    service = ServiceArchive.objects.get(id=pk)
    restore = Service.objects.create(id=pk,name=service.name,category=service.category,
                                             labor=service.labor,image=service.image,
                                             remarks=service.remarks)
    restore.save()
    messages.success(request,f"{service.name} has been successfully restored.")
    add_activity(logged_user=request.user,activity_type='RESTORE',activity_location='SERVICE',activity_message=f"{service.name} has been successfully restored.")
    service.delete()
    
    return redirect('inventory-service')


# CAR -----------------------------------------------------------------------------------
class CarView(LoginRequiredMixin, SingleTableMixin, CreateView, ExportMixin, ExportPDF, FilterView):
    table_class = CarTable
    filterset_class = CarFilter
    form_class = CarForm
    queryset = Car.objects.values()
    paginate_by = 10
    state = 'inventory'
    label = 'Car'
    inventorypage_active = 'car'
    inventorystatus_active ='active'
    export_formats = ('xlsx','pdf')
    exclude_columns = ('id','description')
    export_name = f"Car_List_Report_{strftime('%Y-%m-%d', localtime())}"
    dataset_kwargs = {"title": "Car"}
    
    def get_context_data(self, *args, **kwargs):
        context = super(CarView, self).get_context_data(*args, **kwargs)
        context['notifications'] = Notifications.objects.filter(user=self.request.user)
        return context
    
    def get_template_names(self):
        
        return 'partials/table.html' if self.request.htmx else 'inventory/car.html'
    
    def form_valid(self, form):
        messages.success(self.request, 
                         f'Car {self.request.POST.get("make")} {self.request.POST.get("model")} {self.request.POST.get("sub_model")} {self.request.POST.get("year")} has been created.')
        add_activity(logged_user=self.request.user,activity_type='ADD',activity_location='CAR',
                     activity_message=f'{self.request.POST.get("make")} {self.request.POST.get("model")} {self.request.POST.get("sub_model")} {self.request.POST.get("year")} has been added.')
        form.save()
        
        return redirect('inventory-car')


class CarArchivedView(CarView):
    table_class = CarArchiveTable
    filterset_class = CarArchiveFilter
    queryset = CarArchive.objects.values()
    label = 'Car Archive'
    inventorystatus_active ='archive'
    export_name = f"Car_Archive_List_Report_{strftime('%Y-%m-%d', localtime())}"
    dataset_kwargs = {"title": "Car Archive"}

    def get_template_names(self):
    
        return 'partials/table.html' if self.request.htmx else 'inventory/car_archived.html'


class CarUpdateView(LoginRequiredMixin, SingleTableMixin, UpdateView):
    table_class = CarTable
    form_class = CarForm
    queryset = Car.objects.all()
    paginate_by = 10
    state = 'inventory'
    label = 'Car'
    modal = 'update'
    template_name = 'inventory/car.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(CarUpdateView, self).get_context_data(*args, **kwargs)
        context['notifications'] = Notifications.objects.filter(user=self.request.user)
        return context
        
    def form_valid(self, form):
        messages.success(self.request, 
                         f'Car {self.request.POST.get("make")} {self.request.POST.get("model")} {self.request.POST.get("sub_model")} {self.request.POST.get("year")} has been updated.')
        add_activity(logged_user=self.request.user,activity_type='UPDATE',activity_location='CAR',
                     activity_message=f'{self.request.POST.get("make")} {self.request.POST.get("model")} {self.request.POST.get("sub_model")} {self.request.POST.get("year")} has been updated.')
        form.save()
        
        return redirect('inventory-car')
    
    
@login_required
def car_archive(request,pk):
    car = Car.objects.get(id=pk)
    archive = CarArchive.objects.create(id=pk,make=car.make,model=car.model,
                                             sub_model=car.sub_model,year=car.year,
                                             color=car.color,engine=car.engine,description=car.description)
    archive.save()
    messages.success(request,f"{car.make} {car.model} {car.sub_model} {car.year} has been successfully archived.")
    add_activity(logged_user=request.user,activity_type='ARCHIVE',activity_location='CAR',activity_message=f"{car.make} {car.model} {car.sub_model} {car.year} has been successfully archived.")
    car.delete()
    return redirect('inventory-car-archived')


@login_required
def car_restore(request,pk):
    car = CarArchive.objects.get(id=pk)
    restore = Car.objects.create(id=pk,make=car.make,model=car.model,
                                             sub_model=car.sub_model,year=car.year,
                                             color=car.color,engine=car.engine,description=car.description)
    restore.save()
    messages.success(request,f"{car.make} {car.model} {car.sub_model} {car.year} has been successfully restored.")
    add_activity(logged_user=request.user,activity_type='RESTORE',activity_location='CAR',activity_message=f"{car.make} {car.model} {car.sub_model} {car.year} has been successfully restored.")
    car.delete()
    
    return redirect('inventory-car')
    
    
# SUPPLIER -----------------------------------------------------------------------------------
class SupplierView(LoginRequiredMixin, SingleTableMixin, CreateView, ExportMixin, ExportPDF, FilterView):
    table_class = SupplierTable
    filterset_class = SupplierFilter
    form_class = SupplierForm
    queryset = Supplier.objects.values()
    paginate_by = 10
    state = 'inventory'
    label = 'Supplier'
    inventorypage_active = 'supplier'
    inventorystatus_active ='active'
    export_formats = ('xlsx','pdf')
    exclude_columns = ('id',)
    export_name = f"Supplier_List_Report_{strftime('%Y-%m-%d', localtime())}"
    dataset_kwargs = {"title": "Supplier List"}
    
    def get_context_data(self, *args, **kwargs):
        context = super(SupplierView, self).get_context_data(*args, **kwargs)
        context['notifications'] = Notifications.objects.filter(user=self.request.user)
        return context
    
    def get_template_names(self):
        
        return 'partials/table.html' if self.request.htmx else 'inventory/supplier.html'
    
    def form_valid(self, form):
        messages.success(self.request, f'Supplier {self.request.POST.get("name")} has been created.')
        add_activity(logged_user=self.request.user,activity_type='ADD',activity_location='SUPPLIER',activity_message=f'{self.request.POST.get("name")} has been added.')
        form.save()
        
        return redirect('inventory-supplier')
    

class SupplierArchiveView(SupplierView):
    table_class = SupplierArchiveTable
    filterset_class = SupplierArchiveFilter
    queryset = SupplierArchive.objects.values()
    label = 'Supplier Archive'
    inventorystatus_active ='archive'
    export_name = f"Supplier_Archive_List_Report_{strftime('%Y-%m-%d', localtime())}"
    dataset_kwargs = {"title": "Supplier Archive"}
    
    def get_template_names(self):
        
        return 'partials/table.html' if self.request.htmx else 'inventory/supplier_archived.html'
        

class SupplierUpdateView(LoginRequiredMixin, SingleTableMixin, UpdateView):
    table_class = SupplierTable
    form_class = SupplierForm
    queryset = Supplier.objects.all()
    paginate_by = 10
    state = 'inventory'
    label = 'Supplier'
    modal = 'update'
    template_name = 'inventory/supplier.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(SupplierUpdateView, self).get_context_data(*args, **kwargs)
        context['notifications'] = Notifications.objects.filter(user=self.request.user)
        return context
        
    def form_valid(self, form):
        messages.success(self.request, f'Supplier {self.request.POST.get("name")} has been updated.')
        add_activity(logged_user=self.request.user,activity_type='UPDATE',activity_location='SUPPLIER',activity_message=f'{self.request.POST.get("name")} has been updated.')
        form.save()
        
        return redirect('inventory-supplier')


@login_required
def supplier_archive(request,pk):
    supplier = Supplier.objects.get(id=pk)
    archive = SupplierArchive.objects.create(id=pk,name=supplier.name,address=supplier.address,
                                             contact_num=supplier.contact_num,email=supplier.email,
                                             description=supplier.description)
    archive.save()
    messages.success(request,f"Supplier {supplier.name} has been successfully archived.")
    add_activity(logged_user=request.user,activity_type='ARCHIVE',activity_location='SUPPLIER',activity_message=f"{supplier.name} has been successfully archived.")
    supplier.delete()
    
    return redirect('inventory-supplier-archived')


@login_required
def supplier_restore(request,pk):
    supplier = SupplierArchive.objects.get(id=pk)
    restore = Supplier.objects.create(id=pk,name=supplier.name,address=supplier.address,
                                             contact_num=supplier.contact_num,email=supplier.email,
                                             description=supplier.description)
    restore.save()
    messages.success(request,f"Supplier {supplier.name} has been successfully restored.")
    add_activity(logged_user=request.user,activity_type='RESTORE',activity_location='SUPPLIER',activity_message=f"{supplier.name} has been successfully restored.")
    supplier.delete()
    
    return redirect('inventory-supplier')
    

# SHIPMENT -----------------------------------------------------------------------------------
class ShipmentView(LoginRequiredMixin, SingleTableMixin, ExportMixin, ExportPDF, FilterView):
    table_class = ShipmentTable
    filterset_class = ShipmentFilter
    queryset = Shipment.objects.values('id','date','supplier__name','product','quantity','base_price','fees','gross_amount')
    paginate_by = 10
    state = 'inventory'
    label = 'Shipment'
    inventorystatus_active ='active'
    inventorypage_active = 'shipment'
    export_formats = ('xlsx','pdf')
    export_name = f"Shipment_List_Report_{strftime('%Y-%m-%d', localtime())}"
    dataset_kwargs = {"title": "Shipment"}
    
    def get_context_data(self, *args, **kwargs):
        context = super(ShipmentView, self).get_context_data(*args, **kwargs)
        context['notifications'] = Notifications.objects.filter(user=self.request.user)
        return context
    
    def get_template_names(self):
        
        return 'partials/table.html' if self.request.htmx else 'inventory/shipment.html'
    

class ShipmentArchiveView(ShipmentView):
    table_class = ShipmentArchivedTable
    filterset_class = ShipmentArchiveFilter
    queryset = ShipmentArchive.objects.values('id','date','supplier__name','product','quantity','base_price','fees','gross_amount')
    label = 'Shipment Archive'
    inventorystatus_active ='archive'
    export_name = f"Shipment_Archive_List_Report_{strftime('%Y-%m-%d', localtime())}"
    dataset_kwargs = {"title": "Shipment Archive"}
    
    def get_template_names(self):
        
        return 'partials/table.html' if self.request.htmx else 'inventory/shipment_archived.html'
    
    
@login_required
def shipment_archive(request,pk):
    shipment = Shipment.objects.get(id=pk)
    archive = ShipmentArchive.objects.create(id=pk,supplier=shipment.supplier,product=shipment.product,
                                             date=shipment.date,quantity=shipment.quantity,
                                             base_price=shipment.base_price, fees=shipment.fees)
    archive.save()
    shipment.delete()
    messages.success(request,f"Shipment ID: {pk} has been successfully archived.")
    add_activity(logged_user=request.user,activity_type='ARCHIVE',activity_location='SHIPMENT',activity_message=f"Shipment has been successfully archived.")
    
    return redirect('inventory-shipment-archived')


@login_required
def shipment_restore(request,pk):
    shipment = ShipmentArchive.objects.get(id=pk)
    restore = Shipment.objects.create(id=pk,supplier=shipment.supplier,product=shipment.product,
                                             date=shipment.date,quantity=shipment.quantity,
                                             base_price=shipment.base_price, fees=shipment.fees)
    restore.save()
    shipment.delete()
    messages.success(request,f"Shipment ID: {pk} has been successfully restored.")
    add_activity(logged_user=request.user,activity_type='RESTORE',activity_location='SHIPMENT',activity_message=f"Shipment has been successfully restored.")
    
    return redirect('inventory-shipment')



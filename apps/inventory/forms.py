from django import forms
from .models import *
from .widget import DatePickerInput

class ProductForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':4}))
    vendor = forms.CharField(max_length=100, required=True)
    product_type = forms.CharField(max_length=100, required=False)
    tags = forms.CharField(max_length=255, required=False)
    low_stock = forms.IntegerField(min_value=0, required=True, label='Low Stock Limit')
    price = forms.DecimalField(required=True,min_value=1)
    sku = forms.CharField(max_length=100, required=True,label='SKU')
    image = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, 'accept': 'image/png, image/gif, image/jpeg'}))     

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.initial['sku'] = 'N/A'

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('make', 'model', 'sub_model', 'year', 'color', 'engine', 'description')
        

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('name', 'address', 'contact_num', 'email', 'description')
        
        
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'category', 'labor', 'image', 'remarks')
        
        
class AddStockForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ('supplier', 'quantity', 'base_price', 'fees')
        
        
class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ('supplier', 'product', 'quantity', 'base_price', 'fees')
        

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=DatePickerInput)
    end_date = forms.DateField(widget=DatePickerInput)
    start_date.required = False
    end_date.required = False
import django_filters
from django_filters.widgets import RangeWidget
from django.forms.widgets import TextInput, Select

from .models import Car, CarArchive, Service, ServiceArchive, Supplier, SupplierArchive, Shipment, ShipmentArchive


class ServiceFilter(django_filters.FilterSet):
    CATEGORY_CHOICES = [(category,category) for category in Service.objects.values_list('category', flat=True).distinct()]
    
    name = django_filters.CharFilter(label="", lookup_expr="istartswith",widget=TextInput(attrs={'placeholder': 'Name','class':'mr-sm-2'}))
    category = django_filters.ChoiceFilter(label="",choices=CATEGORY_CHOICES,
                                                empty_label=('All Categories'),widget=Select(attrs={'class': 'form-select mr-sm-2'}))

    class Meta:
        model = Service
        fields = ('name', 'category')
        abstract = True


class ServiceArchiveFilter(ServiceFilter):
    
    class Meta(ServiceFilter.Meta):
        model = ServiceArchive


class CarFilter(django_filters.FilterSet):
    make = django_filters.CharFilter(label="", lookup_expr="istartswith",widget=TextInput(attrs={'placeholder': 'Make','class':'mr-sm-2'}))
    model = django_filters.CharFilter(label="", lookup_expr="istartswith",widget=TextInput(attrs={'placeholder': 'Model','class':'mr-sm-2'}))
    sub_model = django_filters.CharFilter(label="", lookup_expr="istartswith",widget=TextInput(attrs={'placeholder': 'Sub-Model','class':'mr-sm-2'}))

    class Meta:
        model = Car
        fields = ('make', 'model', 'sub_model')
        abstract = True
        

class CarArchiveFilter(CarFilter):
    
    class Meta(CarFilter.Meta):
        model = CarArchive


class SupplierFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="", lookup_expr="istartswith",widget=TextInput(attrs={'placeholder': 'Name','class':'mr-sm-2'}))
    contact_num = django_filters.CharFilter(label="", lookup_expr="istartswith",widget=TextInput(attrs={'placeholder': 'Contact No','class':'mr-sm-2'}))
    email = django_filters.CharFilter(label="", lookup_expr="istartswith",widget=TextInput(attrs={'placeholder': 'Email','class':'mr-sm-2'}))

    class Meta:
        model = Supplier
        fields = ('name', 'contact_num', 'email')
        abstract = True


class SupplierArchiveFilter(SupplierFilter):
    
    class Meta(SupplierFilter.Meta):
        model = SupplierArchive


class ShipmentFilter(django_filters.FilterSet):
    product = django_filters.CharFilter(label="", lookup_expr="istartswith",widget=TextInput(attrs={'placeholder': 'Product Name','class':'mr-sm-2'}))
    supplier = django_filters.ModelChoiceFilter(label="",queryset=Supplier.objects.all(),
                                                empty_label=('All Suppliers'),widget=Select(attrs={'class': 'form-select mr-sm-2'}))
    date = django_filters.DateFromToRangeFilter(label="Date: ",widget=RangeWidget(attrs={'type': 'date','class':'textinput textInput form-control mx-sm-2'}))

    class Meta:
        model = Shipment
        fields = ('supplier', 'product')
        abstract = True


class ShipmentArchiveFilter(ShipmentFilter):
    
    class Meta(ShipmentFilter.Meta):
        model = ShipmentArchive
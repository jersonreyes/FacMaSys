import django_filters
from django_filters.widgets import RangeWidget
from django.forms.widgets import TextInput, Select
from django.db.models import Q

from .models import Order

class SalesFilter(django_filters.FilterSet):
    PAYMENT_METHODS = {(payment,payment) for payment in Order.objects.values_list('pay_method', flat=True)}
    
    q = django_filters.CharFilter(method='multiple_filter', label="",widget=TextInput(attrs={'placeholder': 'Search','class':'mr-sm-2'}))
    pay_method = django_filters.ChoiceFilter(label="",choices=PAYMENT_METHODS,
                                                empty_label=('All Payment Methods'),widget=Select(attrs={'class': 'form-select mr-sm-2'}))
    date_created = django_filters.DateFromToRangeFilter(label="Date: ",widget=RangeWidget(attrs={'type': 'date','class':'textinput textInput form-control mx-sm-2'}))

    class Meta:
        model = Order
        fields = ('q','pay_method','date_created')
        abstract = True
        
    def multiple_filter(self, queryset, name, value):
        return queryset.filter(
            Q(invoice_number__istartswith=value) | Q(customer__name__istartswith=value) | Q(staff__username__istartswith=value))
import django_filters
from django.contrib.auth.models import User
from django.forms.widgets import Select, TextInput
from django_filters.widgets import RangeWidget

from .models import ActivityLog


class ActivityFilter(django_filters.FilterSet):
    TYPES = {(t,t) for t in ActivityLog.objects.values_list('type', flat=True)}
    LOCATIONS = {(location,location) for location in ActivityLog.objects.values_list('location', flat=True)}
    
    type = django_filters.ChoiceFilter(label="",choices=TYPES,
                                            empty_label=('All Types'),widget=Select(attrs={'class': 'form-select mr-sm-2'}))
    location = django_filters.ChoiceFilter(label="",choices=LOCATIONS,
                                            empty_label=('All Locations'),widget=Select(attrs={'class': 'form-select mr-sm-2'}))
    user = django_filters.ModelChoiceFilter(label="",queryset=User.objects.all(),
                                            empty_label=('All Users'),widget=Select(attrs={'class': 'form-select mr-sm-2'}))
    datetime = django_filters.DateFromToRangeFilter(label="Date: ",widget=RangeWidget(attrs={'type': 'date','class':'textinput textInput form-control mx-sm-2'}))
    
    class Meta:
        model = ActivityLog
        fields = ('type', 'location','user','datetime')
    
    
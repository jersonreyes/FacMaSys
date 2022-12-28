import django_filters
from django.db.models import Q
from django.forms.widgets import TextInput
from django.contrib.auth.models import User


class FacultyFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='multiple_filter', label="",widget=TextInput(attrs={'placeholder': 'Search','class':'form-control mr-sm-2 bg-transparent dark:placeholder-white dark:white dark:border-[rgba(105,105,105,0.5)]'}))
    
    class Meta:
        model = User
        fields = ('q',)
        
    def multiple_filter(self, queryset, name, value):
        return queryset.filter(
            Q(username__istartswith=value) | Q(first_name__istartswith=value) | Q(last_name__istartswith=value) | Q(email__istartswith=value))
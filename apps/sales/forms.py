from django import forms
from .models import Customer, Order
from .widget import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Row, Submit, Button, Column

class CustomerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('name'), css_class='col-md-6',),
                Div(Field('email'), css_class='col-md-6',),
                css_class='row',
            ),
            Div(
                Div(Field('contact'), css_class='col-md-6',),
                Div(Field('address'), css_class='col-md-6',),
                css_class='row',
            ),
            Div(
                Div(Field('car_make'), css_class='col-md-6',),
                Div(Field('plate_no'), css_class='col-md-6',),
                css_class='row',
            ),
        )
        super(CustomerForm, self).__init__(*args, **kwargs)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer',)
        
class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=DatePickerInput)
    end_date = forms.DateField(widget=DatePickerInput)
    start_date.required = False
    end_date.required = False
    
    
DATE_FILTERS = (
    ("Daily","Daily"),
    ("Weekly","Weekly"),
    ("Monthly","Monthly"),
    ("Yearly","Yearly"),
)

class DateFilterForm(forms.Form):
    date_filter = forms.ChoiceField(choices=DATE_FILTERS)
    date_range = forms.ChoiceField(choices=DATE_FILTERS)
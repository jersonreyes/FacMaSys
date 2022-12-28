from django import forms
from .models import EmailNotification
from .models import *
from bootstrap_datepicker_plus.widgets import TimePickerInput, DatePickerInput

class NotificationForm(forms.ModelForm):
    notification = forms.BooleanField(label='Enable Notifications',required=False)
    class Meta:
        model = EmailNotification
        fields = ('notification', 'frequency', 'time', 'day')
        widgets = {
            "time": TimePickerInput(),
            "day": DatePickerInput(),
        }


class StoreForm(forms.ModelForm):
    class Meta:
        model = StoreInfo
        fields = ('email','address','telephone')
        



# class CreateUserForm(UserCreationForm):
#     email = forms.EmailField(required=True)
    
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')
        
        
# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField(required=True)
#     class Meta:
#         model = User
#         fields = ('username', 'email')
        
# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('address', 'phone', 'image')

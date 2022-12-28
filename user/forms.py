from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'remember_me')
        

class RegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password1', 'password2')
        
        
class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        
class ProfileUpdateForm(forms.ModelForm):
    age = forms.IntegerField(min_value=10, max_value=200, required=False)
    
    class Meta:
        model = Profile
        fields = ('user_role', 'age', 'address', 'city_of_residence', 'phone', 'image')
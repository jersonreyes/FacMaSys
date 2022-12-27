from django.shortcuts import render, redirect
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from speedlabproject.utils import add_activity
from django.contrib.auth.views import PasswordChangeView
from time import strftime, localtime
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Customer, Profile
from sales.models import Order
from reports.models import Notifications

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username}. Continue to Log In')
            add_activity(logged_user=request.user,activity_type='ADD',activity_location='USER',activity_message=f'Account has been created for {username}.')
            return redirect('user-login')
    else:
        form = CreateUserForm()
    context = {
        'form':form,
        'notifications':Notifications.objects.filter(user=request.user),
    }
    return render(request, 'user/register.html', context)

@login_required
def profile(request):
    return render(request, 'user/profile.html')


@login_required
def profile_update(request):
    if request.method=="POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            name = request.user.username
            add_activity(logged_user=request.user,activity_type='UPDATE',activity_location='USER',activity_message=f'Account has been updated for {name}.')
            messages.success(request,f"{name} your profile has been successfully updated.")
            return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'notifications':Notifications.objects.filter(user=request.user),
        'user_form':user_form,
        'profile_form':profile_form,
    }
    notif = Notifications.objects.create(user=request.user,message=f"Your profile was updated on {strftime('%Y-%m-%d %H:%M:%S', localtime())}")
    notif.save()
    return render(request, 'user/profile_update.html', context)


@login_required
def staff(request):
    if request.user.is_superuser:
        
        if 'q' in request.GET:
            search_customer = request.GET['q']
            multiple_search =  Q(Q(username__istartswith=search_customer)|Q(email__istartswith=search_customer))
            workers = User.objects.filter(multiple_search)
        else:
            workers = User.objects.all()
        page = Paginator(workers,10)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
        context = {
            'label':'Accounts',
            'notifications':Notifications.objects.filter(user=request.user),
            'page':page,
            'count':workers.count(),
            'state':'accounts',
            
        }
        return render(request, 'user/staff.html', context)
    else:
        messages.error(request, f'You are not authorized to access that page. Please login as superuser to be granted access.')
        return redirect('user-login')

@login_required
def customer(request):
    customers = Customer.objects.all()
    if 'q' in request.GET:
        search_customer = request.GET['q']
        multiple_search =  Q(Q(name__istartswith=search_customer)|Q(email__istartswith=search_customer))
        customers = Customer.objects.filter(multiple_search)
    else:
        customers = Customer.objects.all()
        
    page = Paginator(customers,10)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {
        'label':'Accounts',
        'page':page,
        'count':customers.count(),
        'state':'accounts',
        'notifications':Notifications.objects.filter(user=request.user),
        
    }
    return render(request, 'user/customer.html', context)


@login_required
def staff_detail(request, pk):
    worker = User.objects.get(id=pk)
    context = {
        'label':'Accounts',
        'worker':worker,
        'notifications':Notifications.objects.filter(user=request.user),
    }
    return render(request, 'user/staff_detail.html', context)

def customer_detail(request, pk):
    customer = Customer.objects.get(id=pk)
    context = {
        'label':'Accounts',
        'customer': customer,
        'orders': Order.objects.filter(customer=customer),
        'notifications':Notifications.objects.filter(user=request.user),
    }
    return render(request, 'user/customer_detail.html', context)

@login_required
def register_admin(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if request.POST['user-type'] == 'admin':
                user.is_staff=True
            username = form.cleaned_data.get('username')
            user.save()
            notif = Notifications.objects.create(user=request.user,message=f"You created an { request.POST['user-type'] } account for { username } on { strftime('%Y-%m-%d %H:%M:%S', localtime())}")
            notif.save()
            messages.success(request, f'Account has been created for {username}.')
            add_activity(logged_user=request.user,activity_type='ADD',activity_location='USER',activity_message=f'Account has been created for {username}.')
            return redirect('dashboard-staff')
    else:
        form = CreateUserForm()
    context = {
        'form':form,
        'notifications':Notifications.objects.filter(user=request.user),
    }
    return render(request, 'user/register.html', context)


def logout_confirmation(request):
    return render(request, 'user/logout_confirmation.html')



@login_required
def logout_view(request):
    # id = request.user.id
    # user = User.objects.get(id=id)  
    # add_activity(logged_user=user.username,activity_type='LOG OUT',activity_location='LOGOUT FORM',activity_message=f"Successfully Log Out")
    logout(request)
    return render(request, 'user/logout.html')

# class CustomLogin(LoginView):
#     def form_valid(self, form):
#         # name = self.request.user.username
#         # add_activity(logged_user=name,activity_type='LOG IN',activity_location='USER',activity_message=f"{name} Successfully Log In")
#         return super().form_valid(form)

class CustomPasswordChangeView(PasswordChangeView):
    
    def get_context_data(self, *args, **kwargs):
        context = super(CustomPasswordChangeView, self).get_context_data(*args, **kwargs)
        context['notifications'] = Notifications.objects.filter(user=self.request.user)
        return context
    
    def form_valid(self, form):
        name = self.request.user.username
        add_activity(logged_user=self.request.user,activity_type='UPDATE',activity_location='USER',activity_message=f'Account has been updated for {name}.')\
        
        notif = Notifications.objects.create(user=self.request.user,message=f"You changed your password on {strftime('%Y-%m-%d %H:%M:%S', localtime())}")
        notif.save()
        messages.success(self.request,'Your password was successfully updated.')
        return super().form_valid(form)

    
    
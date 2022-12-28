from time import localtime, strftime
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from apps.reports.models import Notifications
from facmasys.utils import add_activity
from .forms import LoginForm, ProfileUpdateForm, RegisterForm, UserUpdateForm


# Create your views here.
class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'user/register.html'


    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect('dashboard-index')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect('user-login')

        return render(request, self.template_name, {'form': form})
    
    
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    

@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('user-login')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('user-profile')
    

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
            messages.success(request,"Your profile has been successfully updated.")
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
def faculty(request):
    if request.user.profile.user_role == 'depthead':
        
        if 'q' in request.GET:
            search_faculty = request.GET['q']
            multiple_search =  Q(Q(username__istartswith=search_faculty)|Q(email__istartswith=search_faculty))
            workers = User.objects.filter(multiple_search)
        else:
            workers = User.objects.filter(profile__user_role='faculty')
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
        return render(request, 'user/faculty.html', context)
    else:
        return redirect('dashboard-index')
    
    
@login_required
def faculty_detail(request, pk):
    worker = User.objects.get(id=pk)
    context = {
        'worker':worker,
        'notifications':Notifications.objects.filter(user=request.user),
    }
    return render(request, 'user/staff_detail.html', context)



# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account has been created for {username}. Continue to Log In')
#             add_activity(logged_user=request.user,activity_type='ADD',activity_location='USER',activity_message=f'Account has been created for {username}.')
#             return redirect('user-login')
#     else:
#         form = RegisterForm()
#     context = {
#         'form':form,
#         'notifications':Notifications.objects.filter(user=request.user),
#     }
#     return render(request, 'user/register.html', context)


# @login_required
# def customer(request):
#     customers = Customer.objects.all()
#     if 'q' in request.GET:
#         search_customer = request.GET['q']
#         multiple_search =  Q(Q(name__istartswith=search_customer)|Q(email__istartswith=search_customer))
#         customers = Customer.objects.filter(multiple_search)
#     else:
#         customers = Customer.objects.all()
        
#     page = Paginator(customers,10)
#     page_list = request.GET.get('page')
#     page = page.get_page(page_list)
#     context = {
#         'label':'Accounts',
#         'page':page,
#         'count':customers.count(),
#         'state':'accounts',
#         'notifications':Notifications.objects.filter(user=request.user),
        
#     }
#     return render(request, 'user/customer.html', context)


# @login_required
# def register_admin(request):
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             if request.POST['user-type'] == 'admin':
#                 user.is_staff=True
#             username = form.cleaned_data.get('username')
#             user.save()
#             notif = Notifications.objects.create(user=request.user,message=f"You created an { request.POST['user-type'] } account for { username } on { strftime('%Y-%m-%d %H:%M:%S', localtime())}")
#             notif.save()
#             messages.success(request, f'Account has been created for {username}.')
#             add_activity(logged_user=request.user,activity_type='ADD',activity_location='USER',activity_message=f'Account has been created for {username}.')
#             return redirect('faculty-index')
#     else:
#         form = CreateUserForm()
#     context = {
#         'form':form,
#         'notifications':Notifications.objects.filter(user=request.user),
#     }
#     return render(request, 'user/register.html', context)
# class CustomPasswordChangeView(PasswordChangeView):
    
#     def get_context_data(self, *args, **kwargs):
#         context = super(CustomPasswordChangeView, self).get_context_data(*args, **kwargs)
#         context['notifications'] = Notifications.objects.filter(user=self.request.user)
#         return context
    
#     def form_valid(self, form):
#         name = self.request.user.username
#         add_activity(logged_user=self.request.user,activity_type='UPDATE',activity_location='USER',activity_message=f'Account has been updated for {name}.')\
        
#         notif = Notifications.objects.create(user=self.request.user,message=f"You changed your password on {strftime('%Y-%m-%d %H:%M:%S', localtime())}")
#         notif.save()
#         messages.success(self.request,'Your password was successfully updated.')
#         return super().form_valid(form)
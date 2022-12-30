from time import localtime, strftime

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django_tables2.export.views import ExportMixin

from apps.feed.models import Feeds
from apps.reports.models import Notifications
from apps.user.models import Profile
from facmasys.models import Research
from facmasys.utils import ExportPDF, add_activity

from .filters import FacultyFilter
# from facmasys.utils import add_activity
from .forms import LoginForm, ProfileUpdateForm, RegisterForm, UserUpdateForm, AddSubjectTaughtForm
from .tables import FacultyTable, FacultyWithResearchTable, FacultyWithExtensionTable

DEV = True

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
            add_activity(activity_type='REGISTER',activity_location='USER',activity_message=f"User {username} has registered.")
            return redirect('user-login')

        return render(request, self.template_name, {'form': form})
    
    
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        add_activity(logged_user=self.request.user,activity_type='LOGIN',activity_location='USER',activity_message=f"User {form.cleaned_data.get('username')} has logged in.")
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
        add_activity(logged_user=request.user,activity_type='LOGOUT',activity_location='USER',activity_message=f"User {request.user.username} has logged out.")
        logout(request)
    return redirect('user-login')


class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('user-profile')
    
    def form_valid(self, form):
        add_activity(logged_user=self.request.user,activity_type='CHANGE PASSWORD',activity_location='USER',activity_message=f"User {self.request.user.username} changed his/her password.")
        return super().form_valid(form)
    

@login_required
def profile(request):
    feeds = list(Feeds.objects.filter(user_id_id=request.user.id).values()),
    researches = list(Research.objects.filter(faculty_id_id=request.user.id).values()),
    context = {
        'feeds': feeds,
        'researches': researches
    }
    return render(request, 'user/profile.html', context)

def profile_viewer(request, id):
    feeds = list(Feeds.objects.filter(user_id_id=id).values()),
    researches = list(Research.objects.filter(faculty_id_id=id).values()),
    user_data = list(User.objects.filter(id=id).values())[0],
    context = {
        'feeds': feeds,
        'view': 'outside',
        'user_data': user_data,
        'researches': researches
    }
    return render(request, 'user/profile.html', context)

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
def del_current_user(request):    
    try:
        add_activity(logged_user=request.user,activity_type='DELETE',activity_location='USER',activity_message=f"User {request.user.username} deleted his/her account.")
        user = request.user
        user.delete()
        messages.success(request, "Your account was deleted.")
        return redirect('index')

    except User.DoesNotExist:
        messages.error(request, "User does not exist")    
        return render('index')


class FacultyView(LoginRequiredMixin, SingleTableMixin, ExportMixin, ExportPDF, FilterView):
    table_class = FacultyTable
    filterset_class = FacultyFilter
    queryset = User.objects.filter(profile__user_role='faculty').values('id','first_name','last_name','username','email','profile', 'profile__spec_track')
    paginate_by = 10
    state = 'accounts'
    label = 'Faculty'
    export_formats = ('xlsx','pdf')
    export_name = f"Faculty_List_Report_{strftime('%Y-%m-%d', localtime())}"
    dataset_kwargs = {"title": "Faculty"}
    
    def get_template_names(self):

        return 'partials/table.html' if self.request.htmx else 'user/faculty.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.user_role == 'faculty':
            return redirect('dashboard-index')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        if (search := request.GET.get('q')) != None:
            self.label += f' filtered by {search}'
            
        return super().get(request)
    

class FacultyWithResearchView(LoginRequiredMixin, SingleTableMixin, ExportMixin, ExportPDF, FilterView):
    table_class = FacultyWithResearchTable
    filterset_class = FacultyFilter
    queryset = User.objects.filter(profile__user_role='faculty').values('id','first_name','last_name','username','email','profile').annotate(number_of_research=Count('research')).filter(number_of_research__gt=0)
    paginate_by = 10
    state = 'accounts'
    label = 'Faculty'
    export_formats = ('xlsx','pdf')
    export_name = f"Faculty_List_Report_{strftime('%Y-%m-%d', localtime())}"
    dataset_kwargs = {"title": "Faculty"}
    
    def get_template_names(self):

        return 'partials/table.html' if self.request.htmx else 'user/faculty.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.user_role == 'faculty':
            return redirect('dashboard-index')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        if (search := request.GET.get('q')) != None:
            self.label += f' filtered by {search}'
            
        return super().get(request)
    

class FacultyWithExtensionView(LoginRequiredMixin, SingleTableMixin, ExportMixin, ExportPDF, FilterView):
    table_class = FacultyWithExtensionTable
    filterset_class = FacultyFilter
    queryset = User.objects.filter(profile__user_role='faculty').values('id','first_name','last_name','username','email','profile').annotate(number_of_extension=Count('extensionservice')).filter(number_of_extension__gt=0).distinct()
    paginate_by = 10
    state = 'accounts'
    label = 'Faculty'
    export_formats = ('xlsx','pdf')
    export_name = f"Faculty_List_Report_{strftime('%Y-%m-%d', localtime())}"
    dataset_kwargs = {"title": "Faculty"}
    
    def get_template_names(self):

        return 'partials/table.html' if self.request.htmx else 'user/faculty.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.user_role == 'faculty':
            return redirect('dashboard-index')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        if (search := request.GET.get('q')) != None:
            self.label += f' filtered by {search}'
            
        return super().get(request)
        
        
@login_required
def add_to_dept(request, pk):
    my_department = request.user.profile.spec_track
    user = User.objects.get(id=pk)
    user.profile.spec_track = my_department
    user.save()
    return redirect('faculty-index')


def add_subject_taught(request, pk):
    user = User.objects.get(id=pk)
    if request.method == "POST":
        form = AddSubjectTaughtForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('faculty-index')
    else:
        form = AddSubjectTaughtForm(instance=user.profile)
    context = {
        'subjectform':form,
    }
    return render(request, 'user/faculty_addsubject.html',context)

    
@login_required
def faculty_detail(request, pk):
    if request.user.profile.user_role == 'faculty':
        return redirect('dashboard-index')
    worker = User.objects.get(id=pk)
    context = {
        'worker':worker,
        'notifications':Notifications.objects.filter(user=request.user),
    }
    return render(request, 'user/faculty_detail.html', context)

@login_required
def get_user(request, id): # May include more arguments depending on URL parameters
    """user = list(Profile.objects.filter(id = id).values())[0]"""
    return JsonResponse(list(User.objects.filter(id = id).values()), safe=False)

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
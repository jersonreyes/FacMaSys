from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views
from user.forms import LoginForm

urlpatterns = [
    path('login/', views.LoginView.as_view(redirect_authenticated_user=True, template_name='user/login.html',
                                           authentication_form=LoginForm), name='user-login'),
    path('register/', views.RegisterView.as_view(), name='user-register'),
    
    path('logout_confirmation/',views.logout_confirmation, name='logout_confirmation'),
    path('logout/', views.logout_view, name='user-logout'),
    path('logout1', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='user-logout1'),
    
    path('profile/', views.profile, name='user-profile'),
    path('profile/update', views.profile_update, name='user-profile-update'),
    
    path('accounts/staff',views.staff, name='dashboard-staff'),
    path('accounts/customer',views.customer, name='dashboard-customer'),
    
    path('staff/detail/<int:pk>/',views.staff_detail, name='dashboard-staff-detail'),
    path('customer/detail/<int:pk>/',views.customer_detail, name='user-customer-detail'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_sent.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_form.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_done.html'), name='password_reset_complete'),
    
    path('password_change/', views.ChangePasswordView.as_view(template_name='user/profile_change_password.html',success_url=reverse_lazy('password_change_done')), name='change-password'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='user/profile.html'), name='password_change_done'),
    
]

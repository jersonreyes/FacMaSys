from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from apps.user.forms import LoginForm

from . import views

urlpatterns = [
    path('get/<int:id>',views.get_user, name="user-get"),
    path('login/', views.LoginView.as_view(redirect_authenticated_user=True, template_name='user/login.html',
                                           authentication_form=LoginForm), name='user-login'),
    path('register/', views.RegisterView.as_view(), name='user-register'),
    
    path('logout/', views.logout_view, name='user-logout'),
    
    path('profile/', views.profile, name='user-profile'),
    path('profile/<int:id>',views.profile_viewer, name="user-profile-view"),
    path('profile/update', views.profile_update, name='user-profile-update'),
    path('profile/delete', views.del_current_user, name='user-profile-delete'),
    path('faculty/',views.FacultyView.as_view(), name='faculty-index'),
    path('faculty/with-research',views.FacultyWithResearchView.as_view(), name='faculty-with-research'),
    path('faculty/with-extension',views.FacultyWithExtensionView.as_view(), name='faculty-with-extension'),
    
    path('faculty/detail/<int:pk>/',views.faculty_detail, name='faculty-index-detail'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_sent.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_form.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_done.html'), name='password_reset_complete'),
    
    path('password_change/', views.ChangePasswordView.as_view(template_name='user/profile_change_password.html',success_url=reverse_lazy('password_change_done')), name='change-password'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='user/profile.html'), name='password_change_done'),
    
]

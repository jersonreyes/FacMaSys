"""facmasys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

handler400 = 'facmasys.views.bad_request'
handler403 = 'facmasys.views.permission_denied'
handler404 = 'facmasys.views.page_not_found'
handler500 = 'facmasys.views.server_error'

urlpatterns = [
    # FacMyLyfe
    # path('accounts/', include('users.urls')),
    # path('user/', include('apps.faculty_member.urls')),
    # path('department_head/', include('apps.department_head.urls')),
    # path('research_coord/', include('apps.research_coord.urls')),
    # path('extension_coord/', include('apps.extension_coord.urls')),
    # FacMyLyfe
    
    path('', views.faculty_member_main), # subject is the default one.
    path('subject_taught/', views.faculty_subjects_taught),
    path('subject_taught/add_subject', views.add_taught_subjects),
    path('subject_taught/update_taught_subjects/<int:id>', views.update_taught_subjects),
    
    path('', views.index, name='index'),
    path('dashboard/', include('apps.dashboard.urls')),
    path('researches/', include('apps.researches.urls')),
    path('feed/', include('apps.feed.urls')),
    path('admin/', admin.site.urls),
    path('export/', include('apps.reports.urls')),
    path('user/', include('apps.user.urls')),
    path("__reload__/", include("django_browser_reload.urls")),

    # path('', views.index),
    path('show_summary_subjects/', views.show_dept_summary),
    path('announcements/', views.show_announcements),
    path('announcements/add_announcements', views.add_announcements),
    path('announcements/update/<int:id>', views.update_announcements),
    path('announcements/delete/<int:id>', views.delete_announcements),
    
    path('extension_services/', views.faculty_extension_services),
    path('extension_services/add_service', views.add_extension_services),
    path('extension_services/edit_service/<int:id>', views.edit_extension_services),
    path('extension_services/update_service/<int:id>', views.update_extension_services),
    path('extension_services/delete_service/<int:id>', views.delete_extension_services),

    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


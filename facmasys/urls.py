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
    
<<<<<<< HEAD
    path('', views.faculty_member_main), # subject is the default one.
    
    
    path('subjects', views.show_subject),
    path('subjects/add_subjects', views.add_subject),
    path('subjects/update_subjects/', views.updateform_subject),
    path('subjects/update_subjects/<int:id>', views.update_subject),
    path('subjects/delete_subjects/<int:id>', views.delete_subject),
    
    
=======
    path('faculty_index/', views.faculty_member_main), # subject is the default one.
>>>>>>> 17cad4acefb0f1e7d31ab5e3f144ee53a509b05d
    path('subject_taught/', views.faculty_subjects_taught),
    path('subject_taught/update_taught_subjects', views.add_taught_subjects),
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

    path('research/', views.faculty_researches),
    path('research/add_research', views.add_researches),
    path('research/add_presented', views.add_presented),
    path('research/add_published', views.add_published),


    path('research/edit_research/<int:id>', views.edit_researches),
    path('research/update_research/<int:id>', views.update_researches),
    path('research/delete_research/<int:id>', views.delete_researches),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


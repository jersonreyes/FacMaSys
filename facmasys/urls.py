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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    # FacMyLyfe
    # path('accounts/', include('users.urls')),
    path('user/', include('apps.faculty_member.urls')),
    path('department_head/', include('apps.department_head.urls')),
    path('research_coord/', include('apps.research_coord.urls')),
    path('extension_coord/', include('apps.extension_coord.urls')),
    # FacMyLyfe
    
    path('', views.index, name='index'),
    path('dashboard/', include('apps.dashboard.urls')),
    path('researches/', include('apps.researches.urls')),
    path('feed/', include('apps.feed.urls')),
    path('admin/', admin.site.urls),
    path('export/', include('apps.reports.urls')),
    path('user/', include('apps.user.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


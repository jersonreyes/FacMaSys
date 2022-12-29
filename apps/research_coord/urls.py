from django.urls import path
from . import views

# Research Coordinator URLS
urlpatterns = [
    path('', views.index),
    path('show_summary_faculty/', views.show_ext_summary),
    path('announcements/', views.show_announcements),
    path('announcements/update/<int:id>', views.update_announcements),
    path('announcements/delete/<int:id>', views.delete_announcements),
]
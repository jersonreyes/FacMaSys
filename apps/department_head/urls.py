from django.urls import path
from . import views

# Research Coordinator URLS
urlpatterns = [
    path('', views.index),
    path('show_summary_subjects/', views.show_dept_summary),
    path('announcements/', views.show_announcements),
    path('announcements/add_announcements', views.add_announcements),
    path('announcements/update/<int:id>', views.update_announcements),
    path('announcements/delete/<int:id>', views.delete_announcements),
]
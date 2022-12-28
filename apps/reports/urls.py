from django.urls import path
from . import views

urlpatterns = [
    # path('analytics/pdf',views.export_graphs_pdf, name='export-graph-pdf'),
    path('settings/',views.view_settings, name='settings_view'),
    path('settings/activitylog',views.ActivityView.as_view(), name='settings'),
    path('notif/delete/<int:pk>/',views.delete_notification, name='notif-delete'),
    path('notif/delete/all',views.delete_all_notification, name='notif-delete-all'),
]

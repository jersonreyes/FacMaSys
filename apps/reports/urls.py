from django.urls import path

from . import views

urlpatterns = [
    # path('analytics/pdf',views.export_graphs_pdf, name='export-graph-pdf'),
    path('',views.view_reports.as_view(), name='reports_view'),
    path('log',views.ActivityView.as_view(), name='activity_logs'),
    # path('settings/activitylog',views.ActivityView.as_view(), name='settings'),
    path('notif/delete/<int:pk>/',views.delete_notification, name='notif-delete'),
    path('notif/delete/all',views.delete_all_notification, name='notif-delete-all'),
]


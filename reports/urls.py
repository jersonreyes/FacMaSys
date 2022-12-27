from django.urls import path
from . import views

urlpatterns = [
    path('customer/pdf/<int:pk>/',views.exportcustomer_pdf, name='exportcustomer-pdf'),
    
    path('product/excel',views.exportproduct_excel, name='exportproduct-excel'),
    path('product/pdf',views.exportproduct_pdf, name='exportproduct-pdf'),
    
    path('analytics/pdf',views.export_graphs_pdf, name='export-graph-pdf'),
    path('settings/',views.view_settings, name='settings_view'),
    path('settings/activitylog',views.ActivityView.as_view(), name='settings'),
    path('settings/storeinfo',views.store_info, name='store'),
    path('settings/storeinfo_change',views.store_info_change, name='storechange'),
    
    path('notif/delete/<int:pk>/',views.delete_notification, name='notif-delete'),
    path('notif/delete/all',views.delete_all_notification, name='notif-delete-all'),
    
    path('notification/settings',views.notif_view, name='notif-view'),
    path('notification/update',views.notif_update, name='notif-update'),
    
    path('email',views.email_notify, name='notif-email'),
    
    
]

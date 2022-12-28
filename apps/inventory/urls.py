from django.urls import path
from . import views

urlpatterns = [
    path('product/',views.product, name='inventory-product'),
    path('product/search',views.product_search, name='inventory-product-search'),
    
    path('product/all',views.product_all, name='inventory-product-all'),
    path('product/active',views.product_active, name='inventory-product-active'),
    path('product/out',views.product_out, name='inventory-product-out'),
    path('product/archived',views.product_archived, name='inventory-product-archived'),
    
    path('product/addstock/<int:pk>/',views.add_stock, name='inventory-product-add-stock'),
    path('product/update/<int:pk>/',views.product_update, name='inventory-product-update'),
    path('product/view/<int:pk>/',views.product_view, name='inventory-product-view'),
    path('product/archive/<int:pk>/',views.product_archive, name='inventory-product-archive'),
    path('product/restore/<int:pk>/',views.product_restore, name='inventory-product-restore'),
    
    path('car/',views.CarView.as_view(), name='inventory-car'),
    path('car/archived',views.CarArchivedView.as_view(), name='inventory-car-archived'),
    path('car/update/<int:pk>/',views.CarUpdateView.as_view(), name='inventory-car-update'),
    path('car/archive/<int:pk>/',views.car_archive, name='inventory-car-archive'),
    path('car/restore/<int:pk>/',views.car_restore, name='inventory-car-restore'),
    
    
    path('supplier/',views.SupplierView.as_view(), name='inventory-supplier'),
    path('supplier/archived',views.SupplierArchiveView.as_view(), name='inventory-supplier-archived'),
    path('supplier/update/<int:pk>/',views.SupplierUpdateView.as_view(), name='inventory-supplier-update'),
    path('supplier/archive/<int:pk>/',views.supplier_archive, name='inventory-supplier-archive'),
    path('supplier/restore/<int:pk>/',views.supplier_restore, name='inventory-supplier-restore'),
    
    
    path('service/',views.ServiceView.as_view(), name='inventory-service'),
    path('service/archived',views.ServiceArchiveView.as_view(), name='inventory-service-archived'),
    path('service/update/<int:pk>/',views.ServiceUpdateView.as_view(), name='inventory-service-update'),
    path('service/archive/<int:pk>/',views.service_archive, name='inventory-service-archive'),
    path('service/restore/<int:pk>/',views.service_restore, name='inventory-service-restore'),
    
    path('shipment/',views.ShipmentView.as_view(), name='inventory-shipment'),
    path('shipment/archived',views.ShipmentArchiveView.as_view(), name='inventory-shipment-archived'),
    path('shipment/archive/<int:pk>/',views.shipment_archive, name='inventory-shipment-archive'),
    path('shipment/restore/<int:pk>/',views.shipment_restore, name='inventory-shipment-restore'),

    

          
]

# htmx_urlpatterns = [
#     path('product-search/',views.product_search, name='product-search'),
# ]

# urlpatterns += htmx_urlpatterns
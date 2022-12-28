from django.urls import path
from . import views

urlpatterns = [
    path('',views.SalesView.as_view(), name='sales'),
    path('returned',views.SalesReturnedView.as_view(), name='sales-returned'),
    path('return/<int:pk>/',views.sales_return, name='sales-return'),
    
    path('addcart/product/<int:pk>/',views.add_cart_product, name='add-cart-product'),
    path('addcart/service/<int:pk>/',views.add_cart_service, name='add-cart-service'),
    
    path('deletecart/product/<int:pk>/',views.delete_cart_product, name='delete-cart-product'),
    path('deletecart/service/<int:pk>/',views.delete_cart_service, name='delete-cart-service'),
    
    path('order/product/search',views.order_product_search, name='order-product-search'),
    path('order/service/search',views.order_service_search, name='order-service-search'),
    
    path('order/',views.order, name='order'),
    path('order/add',views.add_order, name='add-order'),
    
    path('analytics/',views.analytics, name='analytics'),
    path('analytics/filter',views.graphs, name='graphs'),
    
    path('customer/detail/<int:pk>/',views.customer_detail, name='sales-customer-detail'),
]

from django.contrib import admin
from .models import *


class CartAdmin(admin.ModelAdmin):
    readonly_field = 'subtotal'
    
class OrderAdmin(admin.ModelAdmin):
    field = 'date_created'
    
# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(OrderProductArchive)
admin.site.register(OrderService)
admin.site.register(OrderServiceArchive)
admin.site.register(CartProduct)
admin.site.register(CartService)
admin.site.register(Cart, CartAdmin)
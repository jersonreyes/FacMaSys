from django.contrib import admin
from .models import *


class ShipmentAdmin(admin.ModelAdmin):
    readonly_fields = ('date', 'gross_amount')

# Register your models here.
admin.site.register(Service)
admin.site.register(ServiceArchive)
admin.site.register(Car)
admin.site.register(CarArchive)
admin.site.register(Supplier)
admin.site.register(SupplierArchive)
admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(ShipmentArchive, ShipmentAdmin)

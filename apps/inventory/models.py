from django.db import models
from django.core.validators import MinValueValidator 
from decimal import Decimal
from django.utils import timezone
from django.db.models.functions import Lower


# Create your models here.
class Car(models.Model):
    make = models.CharField(max_length=100, null=True)
    model = models.CharField(max_length=100, null=True)
    sub_model = models.CharField(max_length=100, null=True)
    year = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=100, null=True)
    engine = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        ordering = (Lower('make'),Lower('model'),Lower('sub_model'),'-year')
    
    def __str__(self) -> str:
        return f'{self.make} {self.model} {self.sub_model} {self.year} {self.engine}'


class CarArchive(models.Model):
    make = models.CharField(max_length=100, null=True)
    model = models.CharField(max_length=100, null=True)
    sub_model = models.CharField(max_length=100, null=True)
    year = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=100, null=True)
    engine = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        ordering = (Lower('make'),Lower('model'),Lower('sub_model'),'-year')
    
    def __str__(self) -> str:
        return f'{self.make} {self.model} {self.sub_model} {self.year} {self.engine}'
    
    
class Service(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    category = models.CharField(max_length=100, null=True)
    labor = models.DecimalField(default=0, max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    image = models.ImageField(default='services.png', upload_to='Service_Images', null=True)
    remarks = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = (Lower('name'),)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    
class ServiceArchive(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    category = models.CharField(max_length=100, null=True)
    labor = models.DecimalField(default=0, max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    image = models.ImageField(default='services.jpg', upload_to='Services_Images', null=True)
    remarks = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = (Lower('name'),)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    
class Supplier(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    address = models.CharField(max_length=255, null=True)
    contact_num = models.CharField(max_length=11, null=True)
    email = models.EmailField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        ordering = (Lower('name'),)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    
class SupplierArchive(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    address = models.CharField(max_length=255, null=True)
    contact_num = models.CharField(max_length=11, null=True)
    email = models.EmailField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        ordering = (Lower('name'),)
        
    def __str__(self) -> str:
        return f'{self.name}'
    

class Shipment(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(default=timezone.now)
    quantity = models.PositiveIntegerField(default=1, null=True)
    base_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    fees = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    gross_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    
    class Meta:
        ordering = ('-date',)
    
    def __str__(self) -> str:
        return f'{self.quantity} {self.product} from {self.supplier} on {self.date.strftime("%Y-%m-%d %I:%M %p")}'
    

class ShipmentArchive(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.CharField(max_length=255, null=True)
    date = models.DateTimeField()
    quantity = models.PositiveIntegerField(default=1, null=True)
    base_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    fees = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    gross_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    
    class Meta:
        ordering = ('-date',)
    
    def __str__(self) -> str:
        return f'{self.quantity} {self.product} from {self.supplier} on {self.date.strftime("%Y-%m-%d %I:%M %p")}'
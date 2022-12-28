from decimal import Decimal
from email.policy import default
from enum import unique

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.forms import ChoiceField
from django.utils import timezone

from apps.inventory.models import Service
from apps.user.models import Customer


# Create your models here.
class OrderProduct(models.Model):
    date = models.DateTimeField(default=timezone.now)
    item_id = models.CharField(max_length=100, null=True)
    product_title = models.CharField(max_length=255, null=True)
    quantity = models.PositiveIntegerField(default=1, null=True)
    price = models.DecimalField(default=1, max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], null=True)
    cost = models.DecimalField(default=1, max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], null=True)
    
    @property
    def total_price(self):
        return f'{float(self.price) * float(self.quantity):.2f}'
    
    def __str__(self) -> str:
        return f'{self.quantity} {self.product_title}'

    
class OrderProductArchive(models.Model):
    date = models.DateTimeField(default=timezone.now)
    item_id = models.CharField(max_length=100, null=True)
    product_title = models.CharField(max_length=255, null=True)
    quantity = models.PositiveIntegerField(default=1, null=True)
    price = models.DecimalField(default=1, max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], null=True)
    cost = models.DecimalField(default=1, max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], null=True)
    
    @property
    def total_price(self):
        return f'{float(self.price) * float(self.quantity):.2f}'
    
    def __str__(self) -> str:
        return f'{self.quantity} {self.product_title}'
    
    
class OrderService(models.Model):
    date = models.DateTimeField(default=timezone.now)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    labor = models.DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    
    def __str__(self) -> str:
        return f'{self.service}'
    
    
class OrderServiceArchive(models.Model):
    date = models.DateTimeField(default=timezone.now)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    labor = models.DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    
    def __str__(self) -> str:
        return f'{self.service}'
    
    
STATUS_CHOICES = (
    ("Completed", "Completed"),
    ("Returned", "Returned")
)
class Order(models.Model):
    PAYMENT_METHODS = (
    ("Cash", "Cash"),
    ("Bank Transfer", "Bank Transfer"),
    ("Credit/Debit", "Credit/Debit"),
    )
    
    invoice_number = models.CharField(max_length=20)
    date_created = models.DateTimeField(default=timezone.now)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(OrderProduct)
    services = models.ManyToManyField(OrderService)
    subtotal = models.DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], null=True)
    vat = models.DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], null=True)
    total = models.DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], null=True)
    pay_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="Cash",blank=False)
    pay_id = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(default="Completed",max_length=20, null=True)
    
    class Meta:
        ordering = ('-date_created',)
        
    def __str__(self) -> str:
        return f'Invoice:{self.invoice_number}'
       
      
class CartProduct(models.Model):
    item_id = models.CharField(max_length=100, null=True)
    product_title = models.CharField(max_length=255, null=True)
    quantity = models.PositiveIntegerField(default=1, null=True)
    price = models.DecimalField(default=0, max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], null=True)
    
    @property
    def total_price(self):
        return self.price * self.quantity
    
    def __str__(self) -> str:
        return f'{self.quantity} {self.product_title}'
    
    
class CartService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    labor = models.DecimalField(default=0, max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    
    def __str__(self) -> str:
        return f'{self.service}'
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(CartProduct)
    service = models.ManyToManyField(CartService)
    
    @property
    def subtotal(self):
        product_sum, service_sum = 0, 0
        product_set, service_set = self.products.all(), self.service.all()
        for cart_product in product_set:
            product_sum += cart_product.price * cart_product.quantity
        for cart_service in service_set:
            service_sum += cart_service.labor
        return float(product_sum) * float(0.88) + float(service_sum)
    
    @property
    def vat(self):
        sum = 0
        product_set = self.products.all()
        for cart_product in product_set:
            sum += cart_product.price * cart_product.quantity
        return f'{float(sum) * 0.12:.2f}'
    
    @property
    def total(self):
        return f'{float(self.subtotal) + float(self.vat):.2f}'
        
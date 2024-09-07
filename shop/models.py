from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=200, null=False)
    image = models.ImageField(upload_to='item_images/')
    # isDigital = models.BooleanField(default=False, null=True, blank=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField(default=0)
    # category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.name 
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self) -> str:
        return str(self.id)
    
class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (self.item.name)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)
    zipcode = models.CharField(max_length=20, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.address
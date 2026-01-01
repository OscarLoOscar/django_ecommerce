from django.db import models
from orders.models import Order
from products.models import Product

# Create your models here.
class OrderItem(models.Model):
  order=models.ForeignKey(Order,on_delete=models.CASCADE, related_name='items')
  product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True) # null=True and on_delete=SET_NULL,when deleted product,OrderItem will keep record
  price = models.DecimalField(max_digits=10, decimal_places=2)
  quantity = models.IntegerField()

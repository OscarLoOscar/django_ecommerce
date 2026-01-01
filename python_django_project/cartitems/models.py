from django.db import models
from carts.models import Cart
from products.models import Product

# Create your models here.
class CartItem(models.Model):
  cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  quantity=models.PositiveIntegerField(default=1)
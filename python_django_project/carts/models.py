from django.db import models
from users.models import User
from products.model import Product
# Create your models here.
class Cart(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE)
  created_at=models.DateTimeField(auto_now_add=True)
  products=models.ManyToManyField(Product,through='CartItem')
  def __str__(self):
    return self.title
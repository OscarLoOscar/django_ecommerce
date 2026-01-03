from django.db import models
from users.models import User
from products.models import Product
# Create your models here.
class Cart(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE)
  created_at=models.DateTimeField(auto_now_add=True)
  list_display = ('id', 'user', 'created_at')
  search_fields = ('id', 'user__name', 'user__email')
  products=models.ManyToManyField(Product,through='cartitems.CartItem')
  def __str__(self):
    return f"Cart ({self.user.name})"
  
class Meta:
  ordering = ['created_at']
  indexes = [models.Index(fields = ['created_at'])]

  def __str__(self):
    return self.user
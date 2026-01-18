from django.db import models
from carts.models import Cart
from products.models import Product

# Create your modelxs here.
class CartItem(models.Model):
  cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  size = models.CharField(max_length=20,default='Standard')
  quantity=models.PositiveIntegerField(default=1)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def get_subtotal(self):
      return self.product.price * self.quantity
  
  def __str__(self):
    return f"{self.product.title} {self.quantity}"

  class Meta:
    ordering=['-created_at']
    indexes = [models.Index(fields=['created_at'])]

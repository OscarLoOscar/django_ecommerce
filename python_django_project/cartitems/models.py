from django.db import models
from carts.models import Cart
from products.models import Product

# Create your modelxs here.
class CartItem(models.Model):
  cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  quantity=models.PositiveIntegerField(default=1)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering=['-created_at']
    indexes = [models.Index(fields=['created_at'])]

    def __str__(self):
      return self.product.title

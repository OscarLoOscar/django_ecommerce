from django.db import models
from orders.models import Order
from products.models import Product

# Create your models here.
class OrderItem(models.Model):
  order=models.ForeignKey(Order,on_delete=models.CASCADE, related_name='items')
  product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True) # null=True and on_delete=SET_NULL,when deleted product,OrderItem will keep record
  price = models.DecimalField(max_digits=10, decimal_places=2)
  quantity = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  size=models.CharField(max_length=20,default="Standard")

  class Meta:
    ordering=['-created_at']
    indexes = [models.Index(fields=['created_at'])]
    

  def __str__(self):
    return self.product.title
  
  # must keep , dashboard can show HK$
  def get_subtotal(self):
    return self.product.price * self.quantity
from django.db import models
from django.conf import settings # use settings.AUTH_USER_MODEL
from products.models import Product
# Create your models here.
class Cart(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE,null=True,blank=True)
  session_id = models.CharField(max_length=100,null=True,blank=True,db_index=True) # db_index = database index will be created 書尾嘅索引表 for this field : filter()： Cart.objects.get(session_id="xxx"), exclude() , order_by()
  created_at=models.DateTimeField(auto_now_add=True)
  products=models.ManyToManyField(Product,through='cartitems.CartItem')

  class Meta:
    ordering = ['created_at']
    indexes = [models.Index(fields = ['created_at']),models.Index(fields=['session_id'])]

  def __str__(self):
    if self.user:
      return F"Cart(User:{self.user.username})"
    return f"Cart (Session: {self.session_id})"

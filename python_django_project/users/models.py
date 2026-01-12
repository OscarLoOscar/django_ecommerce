from django.db import models
from django.contrib.auth.models import AbstractUser
from products.models import Product
# Create your models here.
class User(AbstractUser):
  phone = models.CharField(max_length = 15,blank=True)
  def __str__(self):
    return self.username
  # AbstractUser : username, email, first_name, last_name, password

  # username = models.CharField(max_length=50)
  # email = models.EmailField(max_length=100,unique=True,blank=False)
  # first_name = models.CharField(max_length=10,blank=True,default='')
  # last_name = models.CharField(max_length=30,blank=True,default='')
  # password1 = models.CharField(max_length=30,default='123456')
  # password2 = models.CharField(max_length=30,default='123456')

class PurchaseHistory(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = "Purchase Histories"
    ordering = ['-created_at']
    indexes = [models.Index(fields=['created_at'])]
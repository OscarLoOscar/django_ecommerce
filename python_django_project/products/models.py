from django.db import models
from categories.models import Category
# Create your models here.
class Product(models.Model):
  category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
  title=models.CharField(max_length=200)
  description=models.TextField()
  policy_info=models.TextField()
  price=models.DecimalField(max_digits=10,decimal_places=2)
  stock_count=models.IntegerField(default=0)
  image=models.ImageField(upload_to='products/')

  def __str__(self):
    return self.title
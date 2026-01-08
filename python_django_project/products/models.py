from django.db import models
from categories.models import Category
# Create your models here.
class Product(models.Model):
  TYPE_CHOICE=(
    ('戒指','戒指'),
    ('手鏈', '手鏈'),
    ('頸鏈', '頸鏈'),
    ('媽媽勾織','媽媽勾織')
  )
  category = models.ForeignKey(Category,related_name='products',on_delete=models.PROTECT)
  title=models.CharField(max_length=200)
  description=models.TextField()
  policy_info=models.TextField()
  price=models.DecimalField(max_digits=10,decimal_places=2)
  stock_count=models.IntegerField(default=0)
  size=models.IntegerField(default=11,help_text="戒指預設11，其餘預設0")
  product_type = models.CharField(max_length=10,choices=TYPE_CHOICE,default='戒指')
  image=models.ImageField(upload_to='products/')

  def __str__(self):
    return self.title
  
  def save(self,*args,**kwargs):
    if self.product_type == '戒指':
      if self.size==0 or self.size is None:
        self.size=11
    elif self.product_type in ['手鏈','頸鏈']:
      if self.size == 11:
        self.size=0
    super().save(*args,**kwargs)

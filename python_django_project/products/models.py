from django.db import models
from categories.models import Category
# Create your models here.
class Product(models.Model):
  category = models.ForeignKey(Category,related_name='products',on_delete=models.PROTECT)
  title=models.CharField(max_length=200)
  description=models.TextField()
  policy_info=models.TextField()
  price=models.DecimalField(max_digits=10,decimal_places=2)
  stock_count=models.IntegerField(default=0)
  size=models.IntegerField(default=11,help_text="戒指預設11，其餘預設0")
  image_00=models.ImageField(upload_to='products/',blank=False)
  image_01=models.ImageField(upload_to='products/',blank=True)
  image_02=models.ImageField(upload_to='products/',blank=True)
  image_03=models.ImageField(upload_to='products/',blank=True)
  image_04=models.ImageField(upload_to='products/',blank=True)
  is_published=models.BooleanField(default=True)

  def __str__(self):
    return self.title
  
  def save(self,*args,**kwargs):
    if self.category:
      ctype = self.category.category_type

      if ctype == '戒指':
        if self.size==0 or self.size is None:
          self.size=11
      elif ctype in ['手鏈','頸鏈']:
        if self.size == 11:
          self.size=0
    super().save(*args,**kwargs)

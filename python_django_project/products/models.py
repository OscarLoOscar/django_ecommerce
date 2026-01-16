from django.db import models
from categories.models import Category
from PIL import Image # Pillow, must talk
import os
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
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title
  
  def save(self,*args,**kwargs):
    if self.category:
      ctype = self.category.category_type

      if ctype == ['手鏈','頸鏈']:
        if self.size==11 or self.size is None:
          self.size=0
      elif ctype in '戒指':
        if self.size == 11:
          self.size = 11
    super().save(*args,**kwargs)

    images_to_resize = [self.image_00,self.image_01,self.image_02,self.image_03,self.image_04]

    for img_field in images_to_resize:
      if img_field and os.path.exists(img_field.path):
        img=Image.open(img_field.path)

        if img.height > 500 or img.width > 500:
          output_size = (500,500)
          img.thumbnail(output_size)
          img.save(img_field.path)
    # img = Image.open(self.image_00.path)
    # if img.height > 500 or img.width >500:
    #   output_size=(500,500)
    #   img.thumbnail(output_size)
    #   img.save(self.image_00.path)
    # img.thumbnail vs img.resize:
    # thumbnail: 會幫你維持比例
    # 例如你張相係 1000 x 600，做完會變 500 x 300
    # resize: 會夾硬拉伸
    # 如果你寫死 500x 500，張相會變形
  class Meta:
    ordering=['-created_at']
    indexes = [models.Index(fields=['created_at'])]

    def __str__(self):
      return self.title

from django.db import models

# Create your models here.
class Category(models.Model):
  TYPE_CHOICE=(
    ('耳環', '耳環'),
    ('戒指','戒指'),
    ('手鏈', '手鏈'),
    ('頸鏈', '頸鏈'),
    ('媽媽勾織','媽媽勾織')
  )

  name = models.CharField(max_length=20) # name of show on the webpage ,eg:2026 春季系列
  category_type = models.CharField(
    max_length=20,
    choices=TYPE_CHOICE,
    default='耳環',
    help_text="選擇呢個分類屬於邊種產品，會影響 Size 嘅預設邏輯"
  )
  order=models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.name} ({self.get_category_type_display()})"
  
  class Meta:
    ordering=['-created_at']
    indexes = [models.Index(fields=['created_at'])]

def __str__(self):
  return self.product.title


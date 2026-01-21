from django.db import models
from django.conf import settings
# Create your models here.
class ContactMessage(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,null=True,blank=True)
  name = models.CharField(max_length=100)
  phone = models.CharField(max_length = 15,blank=True,null=True)
  email = models.EmailField(max_length=100)
  subject = models.CharField(max_length=200)
  message = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  is_processed = models.BooleanField(default=False)

  def __str__(self):
    return f"來自 {self.name} 的訊息 - {self.subject}"

  class Meta:
    verbose_name = "聯絡訊息"
    verbose_name_plural = "聯絡訊息管理"
from django.db import models
from users.models import User
# Create your models here.
class Order(models.Model):
  DELIVERY_CHOICES=(
    ('BOOTH','下次 Booth 自取'),
    ('SF','順豐到付')
  )
  PAYMENT_CHOICES=(
    ('CC','信用卡'),
    ('PAYME','Payme'),
    ('ALIPAY','支付寶HK'),
    ('APPLE','Apple Pay')
  )
  
  STATUS_CHOICES = (
    ('Pending','Pending'),
    ('Paid','Paid'),
    ('Shipped','Shipped')
  )
  user=models.ForeignKey(User,on_delete=models.PROTECT)
  total_price=models.DecimalField(max_digits=10,decimal_places=2)
  delivery_method=models.CharField(max_length=20,choices=DELIVERY_CHOICES)
  payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
  created_at = models.DateTimeField(auto_now_add=True)
  is_email_sent = models.BooleanField(default=False)

  class Meta:
    ordering = ['-created_at']
    indexes = [models.Index(fields = ['created_at'])]

  def __str__(self):
      return f"Order {self.id} - {self.user.username}"
  
def update_total_price(self):
    total=sum(item.price * item.quantity for item in self.items.all())
    self.total_price=total
    self.save()
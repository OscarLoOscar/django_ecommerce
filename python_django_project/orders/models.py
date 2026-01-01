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
  
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  total_price=models.DecimalField(max_digits=10,decimal_places=2)
  delivery_method=models.CharField(max_length=20,choices=DELIVERY_CHOICES)
  payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
  status = models.CharField(max_length=20, default='Pending') # Pending, Paid, Shipped
  created_at = models.DateTimeField(auto_now_add=True)
from django.db import models
from django.contrib.auth.models import AbstractUser
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

from django.urls import path
from  . import views

app_name = 'users' 

urlpatterns = [
  path('signin/',views.login,name = 'signin'),
  path('logout/',views.logout,name='logout'),
  path('register/',views.register,name='register'),
  path('dashboard/',views.dashboard,name='dashboard'),
]
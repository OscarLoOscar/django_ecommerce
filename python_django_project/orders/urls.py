from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
  path('checkout/',views.checkout,name='checkout'),
  path('pay-sample/<int:order_id>/',views.simulate_sample,name='simulate_sample')
]
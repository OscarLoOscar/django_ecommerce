from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
  path('checkout/',views.checkout,name='checkout'),
  path('pay-sample/<int:order_id>/',views.simulate_sample,name='simulate_sample'),
  path('payment_proof/<int:order_id>',views.upload_payment_proof,name='payment_receipt'),
]

# Consistency ：
# urls.py 嘅 name
# dashboard.html 嘅 {% url '...' %}
# views.py 裡面對應嘅 function 名 呢三者必須完全吻合。
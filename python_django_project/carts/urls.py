from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
  path('',views.api_add_to_cart,name='view_cart'),
  path('add/<int:product_id>/',views.api_add_to_cart,name='add_to_cart'),
  path('update/<int:product_id>/',views.api_update_cart_item,name='update_cart_item'),
  path('remove/<int:product_id>/',views.remove_from_cart,name='remove_from_cart'),
]
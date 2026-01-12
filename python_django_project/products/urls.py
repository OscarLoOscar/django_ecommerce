from django.urls import path
from . import views
app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='index'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/',views.search,name='search')
]
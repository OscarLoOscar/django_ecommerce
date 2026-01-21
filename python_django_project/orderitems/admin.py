from django.contrib import admin
from .models import OrderItem
# Register your models here.

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'price', 'quantity')
    search_fields = ('product__title' , 'order__id')
    autocomplete_fields = ['product','order']
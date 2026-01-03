from django.contrib import admin
from cartitems.models import CartItem
from .models import Cart

# Register your models here.
class CartItemAdmin(admin.ModelAdmin):
  list_display = ('id', 'get_user', 'product', 'quantity')
  search_fields = ('product__title', 'cart__user__username')
  # 呢兩行會去 check ProductAdmin 同 CartAdmin 有冇 search_fields
  autocomplete_fields = ['product', 'cart']
  def get_user(self, obj):
    return obj.cart.user.username
  get_user.short_description = 'Customer'

admin.site.register(CartItem,CartItemAdmin)
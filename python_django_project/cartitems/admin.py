from django.contrib import admin
from cartitems.models import CartItem

# Register your models here.
class CartItemAdmin(admin.ModelAdmin):
  list_display = ('id', 'get_user', 'product', 'quantity','created_at')
  search_fields = ('product__title', 'cart__user__username')
  # 呢兩行會去 check ProductAdmin 同 CartAdmin 有冇 search_fields
  autocomplete_fields = ['product', 'cart']
  def get_user(self, obj):
    if obj.cart and obj.cart.user:
      return f"{obj.cart.user.username}"
    return f"Visitor{obj.cart.session_id[:8]}"
  
  get_user.short_description = 'User'

admin.site.register(CartItem,CartItemAdmin)
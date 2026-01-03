from django.contrib import admin
from .models import Cart
from cartitems.models import CartItem
# Register your models here.
class CartItemInline(admin.TabularInline):
  model = CartItem
  extra = 0
  autocomplete_fields = ['product']

class CartAdmin(admin.ModelAdmin):
  list_display = 'id','user','created_at','total_items'
  search_fields = ('user__username', 'user__email', 'id')
  inlines = [CartItemInline]

  def total_items(self,obj):
    return obj.products.count()
  total_items.short_description = '產品種類'

admin.site.register(Cart,CartAdmin)
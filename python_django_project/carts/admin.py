from django.contrib import admin
from .models import Cart
from cartitems.models import CartItem
# Register your models here.
class CartItemInline(admin.TabularInline):
  model = CartItem
  extra = 0
  readonly_fields = ('get_price')

  def get_price(self,obj):
    return f"${obj.product.price}"
  get_price.short_description = '單價'

class CartAdmin(admin.ModelAdmin):
  list_display = 'id','user','created_at','item_count'
  search_fields = 'user__name','user__email'
  list_filter = 'created_at'
  inlines = [CartItemInline]

  def item_count(self,obj):
    return obj.products.count()
  item_count.short_description = '產品種類'

admin.site.register(Cart,CartAdmin)
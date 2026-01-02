from django.contrib import admin
from cartitems.models import CartItem
from .models import Cart

# Register your models here.
class CartItemInline(admin.TabularInline):
  model = CartItem
  extra = 1
  autocomplete_field='product'

class CartAdmin(admin.ModelAdmin):
  list_display = 'id','user','created_at','total_items'
  inlines = [CartItemInline]
  def total_items(self,obj):
    return obj.products.count()
  total_items.short_description = '種類數量'

admin.site.register(Cart,CartAdmin)
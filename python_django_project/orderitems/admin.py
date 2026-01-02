from django.contrib import admin
from .models import OrderItem
from orders.models import Order
# Register your models here.
class OrderItemInline(admin.TabularInline):
  model = Order
  extra = 0
  readonly_fields = 'product','price','quantity','get_total'

  def get_total(self,obj):
    return f"{obj.price * obj.total_price}"
  get_total.short_description = '小計'

def total_quantity(self, obj):
    return sum(item.quantity for item in obj.items.all())
total_quantity.short_description = '總件數'

@admin.register(Order)# new written
class OrderItem(admin.ModelAdmin):
  list_display = ('id', 'user', 'total_price', 'status', 'delivery_method', 'created_at')
  list_filter = ('status', 'delivery_method', 'payment_method', 'created_at')
  search_fields = ('user__username', 'user__email', 'id')
  list_editable = ('status',)
  inlines = [OrderItemInline]
# admin.site.register(Order, OrderAdmin) , old written

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'price', 'quantity')
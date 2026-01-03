from django.contrib import admin
from .models import Order
from orderitems.models import OrderItem

# Register your models here.
class OrderItemInline(admin.TabularInline):
  model = OrderItem
  extra = 0
  readonly_fields = 'product','price','quantity','get_total'

  def get_total(self,obj):
    if obj.price and obj.quantity:
      return f"{obj.price * obj.quantity}"
    return "$0"
  get_total.short_description = '小計'

@admin.register(Order)# new written
class OrderAdmin(admin.ModelAdmin):
  list_display = ('id', 'get_user_name', 'total_price', 'status', 'delivery_method', 'created_at','total_quantity')
  list_filter = ('status', 'delivery_method', 'payment_method', 'created_at')
  search_fields = ('user__username', 'user__email', 'id')
  list_editable = ('status',)
  inlines = [OrderItemInline]
# admin.site.register(Order, OrderAdmin) , old written
  def get_user_name(self, obj):
    return obj.user.username
  get_user_name.short_description = 'Customer Name'

  def get_user_email(self, obj):
    return obj.user.email
  get_user_email.short_description = 'Customer Email'

  def total_quantity(self, obj):
    return sum(item.quantity for item in obj.items.all())
  total_quantity.short_description = '總件數'

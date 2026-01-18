from django.contrib import admin
from .models import Order
from orderitems.models import OrderItem
from django.utils.html import format_html # show picture

# Register your models here.
class OrderItemInline(admin.TabularInline):
  model = OrderItem
  extra = 0
  readonly_fields = ('product','price','quantity','get_total')
  fields = ('product','price','quantity','get_total')

  def get_total(self,obj):
    if obj.price and obj.quantity:
      return f"HK${obj.price * obj.quantity}"
    return "$0"
  get_total.short_description = '小計'

@admin.register(Order)# new written
class OrderAdmin(admin.ModelAdmin):
  list_select_related = ('user',)

  list_display = ('id', 'get_user_name', 'total_price', 'status', 'delivery_method','display_payment_receipt','created_at','total_quantity')
  list_filter = ('status', 'delivery_method', 'payment_method', 'created_at')
  search_fields = ('user__username', 'user__email', 'id')
  list_editable = ('status',)
  inlines = [OrderItemInline]

  # add fieldsets @ 18/01/2026
  fieldsets = (('基本資訊',{'fields':('id','user','status','total_price')}),
              ('送貨與付款',{'fields':('delivery_method', 'payment_method', 'shipping_location', 'sf_region', 'sf_address')}),
              ('入數證明',{'fields':('payment_receipt', 'display_payment_receipt', 'payment_receipt_uploaded_at')}))
  
  readonly_fields = ('id', 'created_at', 'display_payment_receipt', 'payment_receipt_uploaded_at')
  # add actions @ 18/01/2026
  # Actions
  actions = ['make_paid','make_shipping','make_shipped']

  @admin.action(description='將選取的訂單改為：已付款 (Paid)')
  def make_paid(self,request,queryset):
    queryset.update(status='Paid')

  @admin.action(description='將選取的訂單改為：發貨中 (Shipping)')
  def make_shipping(self,request,queryset):
    queryset.update(status='Shipping')

  @admin.action(description='將選取的訂單改為：已出貨 (Shipped)')
  def make_shipped(self,request,queryset):
    queryset.update(status='Shipped')
  # Customer Methods
  def display_payment_receipt(self,obj):
    if obj.payment_receipt:
      return format_html('<a href="{}" target="_blank"><img scr="{}" style="width: 100px; height: auto;"/></a> ',
                          obj.payment_receipt.url,obj.payment_receipt.url)
    return "尚未上傳"
  display_payment_receipt.short_description = '入數紙預覽'
  
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

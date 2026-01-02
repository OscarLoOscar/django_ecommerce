from django.contrib import admin
from .models import Order
from users.models import User
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
  list_display = 'id', 'get_user_name', 'get_user_email', 'total_price', 'status', 'created_at'
  search_fields = 'id' ,'user__name', 'user__email'
  list_filter = 'status','delivery_method', 'created_at'
  list_editable = 'status'

  def get_user_name(self,obj):
    return obj.user.name
  get_user_name.short_description = 'Customer Name'

  def get_user_email(self,obj):
    return obj.user.email
  get_user_email.short_description = 'Customer Email'

admin.site.register(Order,OrderAdmin)
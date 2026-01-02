from django.contrib import admin
from .models import User
# Register your models here.
class UsersAdmin(admin.ModelAdmin):
  list_display = 'id','title','price','stock_count','category'
  list_display_links = 'id','title'
  list_editable = 'price','stock_count'
  search_fields = 'title', 'description'
  list_per_page = 25

admin.site.register(User,UsersAdmin)
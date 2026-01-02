from django.contrib import admin
from .models import Product
# Register your models here.
class ProductsAdmin(admin.ModelAdmin):
  list_display = 'id','title','price','stock_count','category'
  list_display_links = 'id','title'
  list_editable = 'price','stock_count'
  search_fields = 'title', 'description'
  list_per_page = 25

admin.site.register(Product,ProductsAdmin)
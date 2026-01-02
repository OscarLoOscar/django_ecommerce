from django.contrib import admin
from .models import Category
from products.models import Product
# Register your models here.
class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ('title', 'price', 'stock_count')
    readonly_fields = ('title', 'price', 'stock_count')

class CategoryAdmin(admin.ModelAdmin):
  list_display = 'id','name','order'
  inlines = [ProductInline]
admin.site.register(Category,CategoryAdmin)
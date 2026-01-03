from django.contrib import admin
from .models import User
# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    # 必須有 search_fields 供 Order/Cart 搜尋
    search_fields = ('username', 'email')
    list_per_page = 25
admin.site.register(User,UsersAdmin)
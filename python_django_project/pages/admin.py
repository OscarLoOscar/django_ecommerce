from django.contrib import admin
from .models import ContactMessage

# Register your models here.
@admin.register(ContactMessage)
class ContactMessage(admin.ModelAdmin):
  list_display= ('name', 'subject', 'email', 'created_at', 'is_processed')
  list_filter = ('is_processed', 'created_at')
  search_fields=('name', 'email', 'subject', 'message')
  readonly_fields = ('created_at',)

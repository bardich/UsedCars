from django.contrib import admin
from .models import CarView, Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'car', 'phone', 'source', 'status', 'created_at']
    list_filter = ['status', 'source', 'created_at']
    search_fields = ['name', 'phone', 'email', 'message']
    list_editable = ['status']
    date_hierarchy = 'created_at'


@admin.register(CarView)
class CarViewAdmin(admin.ModelAdmin):
    list_display = ['car', 'ip_address', 'created_at']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'

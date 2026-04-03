from django.contrib import admin
from .models import User, FinancialRecord

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'status', 'created_at')
    list_filter = ('role', 'status')
    search_fields = ('username', 'email')

@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'category', 'amount', 'created_by')
    list_filter = ('type', 'category', 'date')
    search_fields = ('category', 'notes')
    date_hierarchy = 'date'

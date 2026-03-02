from django.contrib import admin
from .models import Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'user', 'balance', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['account_number', 'user__email', 'user__full_name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'amount', 'status', 'timestamp']
    list_filter = ['status']
    search_fields = ['sender__account_number', 'receiver__account_number', 'idempotency_key']

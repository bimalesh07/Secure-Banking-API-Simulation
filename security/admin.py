from django.contrib import admin
from .models import ActionRequest


@admin.register(ActionRequest)
class ActionRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'action_type', 'target_account',
        'initiated_by', 'status', 'created_at',
    ]
    list_filter = ['status', 'action_type']
    search_fields = [
        'target_account__account_number',
        'initiated_by__email',
    ]

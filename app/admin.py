from django.contrib import admin
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'api_key', 'request_count', 'created_at')
    search_fields = ('username', 'api_key')
    actions = ['regenerate_api_key']

    def regenerate_api_key(self, request, queryset):
        for account in queryset:
            account.regenerate_api_key()

admin.site.register(Account, AccountAdmin)

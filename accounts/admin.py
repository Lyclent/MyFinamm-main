from django.contrib import admin
from accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "balance", "currency", "user")
    search_fields = ("name",)
    list_filter = ("currency",)
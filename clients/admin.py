from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "workspace", "industry", "contact_email", "created_at")
    list_filter = ("workspace", "industry")
    search_fields = ("name", "contact_email", "company_notes")

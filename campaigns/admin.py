from django.contrib import admin
from .models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "status", "start_date", "end_date", "budget", "created_at")
    list_filter = ("status", "client__workspace", "client")
    search_fields = ("title", "objective", "client__name")

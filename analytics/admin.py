from django.contrib import admin
from .models import CampaignMetric


@admin.register(CampaignMetric)
class CampaignMetricAdmin(admin.ModelAdmin):
    list_display = ("campaign", "metric_name", "metric_value", "recorded_date")
    list_filter = ("metric_name", "campaign__client__workspace", "recorded_date")
    search_fields = ("campaign__title", "metric_name")

from django.db import models
from campaigns.models import Campaign


class CampaignMetric(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="metrics")
    metric_name = models.CharField(max_length=100, help_text="e.g. Impressions, Engagement, Clicks, Conversions")
    metric_value = models.DecimalField(max_digits=14, decimal_places=2)
    recorded_date = models.DateField()
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_date", "metric_name"]

    def __str__(self):
        return f"{self.campaign.title} - {self.metric_name}: {self.metric_value}"

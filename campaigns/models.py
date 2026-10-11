from django.db import models
from clients.models import Client


class Campaign(models.Model):
    class Status(models.TextChoices):
        PLANNING = "PLANNING", "Planning"
        ACTIVE = "ACTIVE", "Active"
        PAUSED = "PAUSED", "Paused"
        COMPLETED = "COMPLETED", "Completed"

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="campaigns")
    title = models.CharField(max_length=255)
    objective = models.TextField(help_text="Campaign goal, key message, or target outcome.")
    target_audience = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNING)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.client.name})"

    @property
    def total_content_items(self):
        return self.content_items.count()

    @property
    def published_count(self):
        return self.content_items.filter(status="published").count()

    @property
    def pending_count(self):
        return self.content_items.filter(status__in=["pending_manager", "pending_client"]).count()

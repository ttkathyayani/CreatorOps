from django.db import models
from workspaces.models import Workspace


class Client(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="clients")
    name = models.CharField(max_length=255)
    contact_email = models.EmailField(blank=True, default="")
    industry = models.CharField(max_length=100, blank=True, default="")
    company_notes = models.TextField(blank=True, default="")
    brand_guidelines = models.TextField(
        blank=True,
        default="",
        help_text="Brand voice, required hashtags, compliance rules used by the AI Script Review Agent."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("workspace", "name")

    def __str__(self):
        return f"{self.name} ({self.workspace.name})"

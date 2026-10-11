from django.db import models
from django.contrib.auth.models import User
from content.models import ContentItem


class Asset(models.Model):
    content_item = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name="assets")
    file = models.FileField(upload_to="content_assets/%Y/%m/", blank=True, null=True)
    filename = models.CharField(max_length=255)
    s3_object_key = models.CharField(max_length=500, blank=True, default="")
    mime_type = models.CharField(max_length=100, blank=True, default="")
    size_bytes = models.BigIntegerField(default=0)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.filename} ({self.content_item.title})"

    @property
    def file_size_display(self):
        if self.size_bytes < 1024:
            return f"{self.size_bytes} B"
        elif self.size_bytes < 1024 * 1024:
            return f"{self.size_bytes / 1024:.1f} KB"
        else:
            return f"{self.size_bytes / (1024 * 1024):.1f} MB"

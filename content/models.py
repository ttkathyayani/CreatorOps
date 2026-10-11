from django.db import models
from django.contrib.auth.models import User
from campaigns.models import Campaign


class ContentItem(models.Model):
    class Platform(models.TextChoices):
        INSTAGRAM = "Instagram", "Instagram"
        YOUTUBE = "YouTube", "YouTube"
        LINKEDIN = "LinkedIn", "LinkedIn"
        TWITTER = "Twitter/X", "Twitter/X"
        TIKTOK = "TikTok", "TikTok"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING_MANAGER = "pending_manager", "Pending Manager Review"
        PENDING_CLIENT = "pending_client", "Pending Client Approval"
        APPROVED = "approved", "Approved"
        CHANGES_REQUESTED = "changes_requested", "Changes Requested"
        SCHEDULED = "scheduled", "Scheduled"
        PUBLISHED = "published", "Published"

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="content_items")
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_content"
    )
    title = models.CharField(max_length=255)
    platform = models.CharField(max_length=50, choices=Platform.choices, default=Platform.INSTAGRAM)
    script_body = models.TextField(blank=True, default="", help_text="Draft script / talking points / video storyboard.")
    caption = models.TextField(blank=True, default="", help_text="Final caption, copy, hashtags.")
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.title} [{self.get_platform_display()}] - {self.get_status_display()}"

    def create_version(self, user=None):
        latest = self.versions.order_by("-revision_number").first()
        rev_num = (latest.revision_number + 1) if latest else 1
        return ContentVersion.objects.create(
            content_item=self,
            revision_number=rev_num,
            script_snapshot=self.script_body,
            caption_snapshot=self.caption,
            created_by=user,
        )


class ContentVersion(models.Model):
    content_item = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name="versions")
    revision_number = models.PositiveIntegerField(default=1)
    script_snapshot = models.TextField()
    caption_snapshot = models.TextField(blank=True, default="")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-revision_number"]
        unique_together = ("content_item", "revision_number")

    def __str__(self):
        return f"{self.content_item.title} (v{self.revision_number})"

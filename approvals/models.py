from django.db import models
from django.contrib.auth.models import User
from content.models import ContentItem


class Approval(models.Model):
    class Decision(models.TextChoices):
        MANAGER_APPROVED = "MANAGER_APPROVED", "Manager Approved"
        MANAGER_CHANGES_REQUESTED = "MANAGER_CHANGES_REQUESTED", "Manager Requested Changes"
        CLIENT_APPROVED = "CLIENT_APPROVED", "Client Approved"
        CLIENT_CHANGES_REQUESTED = "CLIENT_CHANGES_REQUESTED", "Client Requested Changes"

    content_item = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name="approvals")
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews")
    decision = models.CharField(max_length=50, choices=Decision.choices)
    comment = models.TextField(help_text="Reviewer feedback, revision notes, or sign-off comment.")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        reviewer_name = self.reviewer.username if self.reviewer else "Unknown"
        return f"{self.content_item.title}: {self.get_decision_display()} by {reviewer_name}"

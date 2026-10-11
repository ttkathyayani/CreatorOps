from rest_framework import serializers
from .models import Approval


class ApprovalSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(source="reviewer.username", read_only=True)
    decision_display = serializers.CharField(source="get_decision_display", read_only=True)

    class Meta:
        model = Approval
        fields = [
            "id",
            "content_item",
            "reviewer",
            "reviewer_username",
            "decision",
            "decision_display",
            "comment",
            "timestamp",
        ]
        read_only_fields = ["id", "reviewer", "timestamp"]

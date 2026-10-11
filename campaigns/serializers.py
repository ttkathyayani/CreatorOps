from rest_framework import serializers
from .models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.name", read_only=True)
    content_count = serializers.IntegerField(source="content_items.count", read_only=True)

    class Meta:
        model = Campaign
        fields = [
            "id",
            "client",
            "client_name",
            "title",
            "objective",
            "target_audience",
            "status",
            "start_date",
            "end_date",
            "budget",
            "content_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

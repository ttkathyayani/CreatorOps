from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    campaigns_count = serializers.IntegerField(source="campaigns.count", read_only=True)

    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "contact_email",
            "industry",
            "company_notes",
            "brand_guidelines",
            "campaigns_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

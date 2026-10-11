from rest_framework import serializers
from .models import ContentItem, ContentVersion


class ContentVersionSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source="created_by.username", read_only=True)

    class Meta:
        model = ContentVersion
        fields = [
            "id",
            "revision_number",
            "script_snapshot",
            "caption_snapshot",
            "created_by_username",
            "created_at",
        ]


class ContentItemSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source="creator.username", read_only=True)
    campaign_title = serializers.CharField(source="campaign.title", read_only=True)
    client_name = serializers.CharField(source="campaign.client.name", read_only=True)
    versions = ContentVersionSerializer(many=True, read_only=True)

    class Meta:
        model = ContentItem
        fields = [
            "id",
            "campaign",
            "campaign_title",
            "client_name",
            "creator",
            "creator_username",
            "title",
            "platform",
            "script_body",
            "caption",
            "due_date",
            "status",
            "versions",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "creator", "created_at", "updated_at"]

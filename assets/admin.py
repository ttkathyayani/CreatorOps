from django.contrib import admin
from .models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("filename", "content_item", "mime_type", "size_bytes", "uploaded_by", "created_at")
    list_filter = ("mime_type", "content_item__campaign__client__workspace")
    search_fields = ("filename", "s3_object_key")

from django.contrib import admin
from .models import ContentItem, ContentVersion


class ContentVersionInline(admin.TabularInline):
    model = ContentVersion
    extra = 0
    readonly_fields = ("revision_number", "created_by", "created_at")


@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = ("title", "campaign", "platform", "status", "creator", "due_date", "updated_at")
    list_filter = ("status", "platform", "campaign__client__workspace", "campaign")
    search_fields = ("title", "script_body", "caption")
    inlines = [ContentVersionInline]


@admin.register(ContentVersion)
class ContentVersionAdmin(admin.ModelAdmin):
    list_display = ("content_item", "revision_number", "created_by", "created_at")
    list_filter = ("content_item__campaign__client__workspace",)

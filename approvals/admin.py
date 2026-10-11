from django.contrib import admin
from .models import Approval


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ("content_item", "decision", "reviewer", "timestamp")
    list_filter = ("decision", "content_item__campaign__client__workspace")
    search_fields = ("comment", "content_item__title", "reviewer__username")

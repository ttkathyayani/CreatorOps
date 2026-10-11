import mimetypes
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from workspaces.permissions import workspace_required
from content.models import ContentItem
from .models import Asset
from .storage import cloud_storage


@workspace_required
def upload_asset(request, content_id):
    item = get_object_or_404(
        ContentItem,
        pk=content_id,
        campaign__client__workspace=request.workspace
    )

    if request.method == "POST" and request.FILES.get("media_file"):
        uploaded = request.FILES["media_file"]

        # Validate file size (max 50 MB)
        if uploaded.size > 50 * 1024 * 1024:
            messages.error(request, "File size exceeds 50MB limit.")
            return redirect("content:detail", pk=content_id)

        mime_type, _ = mimetypes.guess_type(uploaded.name)
        s3_key = f"assets/{request.workspace.id}/{item.id}/{uuid.uuid4().hex}_{uploaded.name}"

        # Attempt S3 upload if configured
        uploaded_s3_key = cloud_storage.upload_file(uploaded, s3_key)

        asset = Asset.objects.create(
            content_item=item,
            file=uploaded,
            filename=uploaded.name,
            s3_object_key=uploaded_s3_key or s3_key,
            mime_type=mime_type or "application/octet-stream",
            size_bytes=uploaded.size,
            uploaded_by=request.user,
        )

        messages.success(request, f"Asset '{asset.filename}' uploaded successfully.")
    else:
        messages.error(request, "Please select a valid media file.")

    return redirect("content:detail", pk=content_id)


@workspace_required
def download_asset(request, pk):
    asset = get_object_or_404(
        Asset,
        pk=pk,
        content_item__campaign__client__workspace=request.workspace
    )

    # If S3 is active, use presigned URL
    presigned = cloud_storage.get_presigned_url(asset.s3_object_key)
    if presigned:
        return HttpResponseRedirect(presigned)

    # Local fallback
    if asset.file:
        return HttpResponseRedirect(asset.file.url)

    messages.error(request, "File not available.")
    return redirect("content:detail", pk=asset.content_item.pk)


@workspace_required
def delete_asset(request, pk):
    asset = get_object_or_404(
        Asset,
        pk=pk,
        content_item__campaign__client__workspace=request.workspace
    )
    content_id = asset.content_item.pk
    filename = asset.filename
    asset.delete()
    messages.success(request, f"Asset '{filename}' removed.")
    return redirect("content:detail", pk=content_id)

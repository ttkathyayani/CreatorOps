from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from workspaces.permissions import workspace_required, role_required, IsWorkspaceMember
from workspaces.models import Membership
from campaigns.models import Campaign
from agents.script_review import ScriptReviewAgent
from agents.approval_summary import ApprovalSummaryAgent
from .models import ContentItem, ContentVersion
from .serializers import ContentItemSerializer


# Template Views
@workspace_required
def content_list(request):
    items = ContentItem.objects.filter(
        campaign__client__workspace=request.workspace
    ).select_related("campaign", "campaign__client", "creator").order_by("-updated_at")

    status_filter = request.GET.get("status")
    platform_filter = request.GET.get("platform")
    campaign_filter = request.GET.get("campaign")

    if status_filter:
        items = items.filter(status=status_filter)
    if platform_filter:
        items = items.filter(platform=platform_filter)
    if campaign_filter:
        items = items.filter(campaign_id=campaign_filter)

    campaigns = Campaign.objects.filter(client__workspace=request.workspace)

    return render(request, "content/list.html", {
        "items": items,
        "campaigns": campaigns,
        "statuses": ContentItem.Status.choices,
        "platforms": ContentItem.Platform.choices,
        "selected_status": status_filter,
        "selected_platform": platform_filter,
        "selected_campaign": campaign_filter,
    })


@workspace_required
def calendar_view(request):
    items = ContentItem.objects.filter(
        campaign__client__workspace=request.workspace,
        due_date__isnull=False
    ).select_related("campaign", "campaign__client")

    return render(request, "calendar/index.html", {
        "items": items,
    })


@workspace_required
def content_detail(request, pk):
    item = get_object_or_404(
        ContentItem.objects.select_related("campaign", "campaign__client", "creator"),
        pk=pk,
        campaign__client__workspace=request.workspace
    )
    versions = item.versions.all().select_related("created_by")
    approvals = item.approvals.all().select_related("reviewer").order_by("-timestamp")
    assets = item.assets.all().select_related("uploaded_by")

    # Run AI Approval Summary if feedback exists
    approval_data = [
        {"reviewer": a.reviewer.username if a.reviewer else "Reviewer", "decision": a.decision, "comment": a.comment}
        for a in approvals
    ]
    summary_agent = ApprovalSummaryAgent()
    approval_summary = summary_agent.run({"approvals": approval_data, "content_title": item.title})

    return render(request, "content/detail.html", {
        "item": item,
        "versions": versions,
        "approvals": approvals,
        "assets": assets,
        "approval_summary": approval_summary,
        "user_role": request.membership.role if request.membership else None,
    })


@workspace_required
@role_required([Membership.Role.ADMIN, Membership.Role.CREATOR, Membership.Role.MANAGER])
def content_create(request):
    campaigns = Campaign.objects.filter(client__workspace=request.workspace)
    if not campaigns.exists():
        messages.warning(request, "Please create a campaign before adding content.")
        return redirect("campaigns:create")

    if request.method == "POST":
        campaign_id = request.POST.get("campaign_id")
        title = request.POST.get("title", "").strip()
        platform = request.POST.get("platform", ContentItem.Platform.INSTAGRAM)
        script_body = request.POST.get("script_body", "").strip()
        caption = request.POST.get("caption", "").strip()
        due_date = request.POST.get("due_date") or None

        campaign = get_object_or_404(Campaign, id=campaign_id, client__workspace=request.workspace)

        if not title:
            messages.error(request, "Content title is required.")
        else:
            item = ContentItem.objects.create(
                campaign=campaign,
                creator=request.user,
                title=title,
                platform=platform,
                script_body=script_body,
                caption=caption,
                due_date=due_date,
                status=ContentItem.Status.DRAFT,
            )
            item.create_version(user=request.user)
            messages.success(request, f"Content draft '{item.title}' created.")
            return redirect("content:detail", pk=item.pk)

    return render(request, "content/form.html", {
        "title": "New Content Script",
        "campaigns": campaigns,
        "platforms": ContentItem.Platform.choices,
    })


@workspace_required
@role_required([Membership.Role.ADMIN, Membership.Role.CREATOR, Membership.Role.MANAGER])
def content_edit(request, pk):
    item = get_object_or_404(ContentItem, pk=pk, campaign__client__workspace=request.workspace)
    campaigns = Campaign.objects.filter(client__workspace=request.workspace)

    if request.method == "POST":
        item.title = request.POST.get("title", "").strip() or item.title
        item.platform = request.POST.get("platform", item.platform)
        old_script = item.script_body
        new_script = request.POST.get("script_body", "").strip()
        item.script_body = new_script
        item.caption = request.POST.get("caption", "").strip()
        item.due_date = request.POST.get("due_date") or None

        item.save()

        # If script changed, preserve revision snapshot
        if old_script != new_script:
            item.create_version(user=request.user)
            messages.info(request, "New script revision recorded in version history.")

        messages.success(request, f"Saved '{item.title}'.")
        return redirect("content:detail", pk=item.pk)

    return render(request, "content/form.html", {
        "title": f"Edit Script: {item.title}",
        "item": item,
        "campaigns": campaigns,
        "platforms": ContentItem.Platform.choices,
    })


@workspace_required
@role_required([Membership.Role.ADMIN, Membership.Role.CREATOR])
def submit_for_review(request, pk):
    item = get_object_or_404(ContentItem, pk=pk, campaign__client__workspace=request.workspace)
    if item.status in [ContentItem.Status.DRAFT, ContentItem.Status.CHANGES_REQUESTED]:
        item.status = ContentItem.Status.PENDING_MANAGER
        item.save()
        messages.success(request, f"'{item.title}' submitted for Manager Review.")
    else:
        messages.warning(request, f"Content item cannot be submitted in status '{item.get_status_display()}'.")
    return redirect("content:detail", pk=item.pk)


@workspace_required
@role_required([Membership.Role.ADMIN, Membership.Role.MANAGER])
def publish_content(request, pk):
    item = get_object_or_404(ContentItem, pk=pk, campaign__client__workspace=request.workspace)
    if item.status == ContentItem.Status.APPROVED:
        item.status = ContentItem.Status.PUBLISHED
        item.save()
        messages.success(request, f"'{item.title}' marked as Published!")
    else:
        messages.error(request, "Only Approved content can be marked as Published.")
    return redirect("content:detail", pk=item.pk)


# REST API ViewSet
class ContentItemViewSet(viewsets.ModelViewSet):
    serializer_class = ContentItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsWorkspaceMember]

    def get_queryset(self):
        ws = getattr(self.request, "workspace", None)
        if ws:
            return ContentItem.objects.filter(campaign__client__workspace=ws).select_related("campaign", "creator")
        return ContentItem.objects.none()

    def perform_create(self, serializer):
        campaign_id = self.request.data.get("campaign")
        campaign = get_object_or_404(Campaign, id=campaign_id, client__workspace=self.request.workspace)
        item = serializer.save(campaign=campaign, creator=self.request.user)
        item.create_version(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="submit")
    def submit(self, request, pk=None):
        item = self.get_object()
        if item.status not in [ContentItem.Status.DRAFT, ContentItem.Status.CHANGES_REQUESTED]:
            return Response(
                {"error": f"Invalid workflow transition from {item.status}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        item.status = ContentItem.Status.PENDING_MANAGER
        item.save()
        return Response({"status": "submitted", "current_status": item.status})


from django.views.decorators.csrf import csrf_exempt

# AI Script Review Endpoint
@csrf_exempt
def api_script_review(request):
    if request.method == "POST":
        import json
        try:
            data = json.loads(request.body)
        except Exception:
            data = request.POST.dict()

        agent = ScriptReviewAgent()
        result = agent.run(data)
        return JsonResponse(result)
    return JsonResponse({"error": "POST required"}, status=405)

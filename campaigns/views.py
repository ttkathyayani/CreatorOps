from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets, permissions
from workspaces.permissions import workspace_required, role_required, IsWorkspaceMember
from workspaces.models import Membership
from clients.models import Client
from .models import Campaign
from .serializers import CampaignSerializer


@workspace_required
def campaign_list(request):
    campaigns = Campaign.objects.filter(
        client__workspace=request.workspace
    ).select_related("client").prefetch_related("content_items")

    status_filter = request.GET.get("status")
    client_filter = request.GET.get("client")

    if status_filter:
        campaigns = campaigns.filter(status=status_filter)
    if client_filter:
        campaigns = campaigns.filter(client_id=client_filter)

    clients = Client.objects.filter(workspace=request.workspace)
    return render(request, "campaigns/list.html", {
        "campaigns": campaigns,
        "clients": clients,
        "statuses": Campaign.Status.choices,
        "selected_status": status_filter,
        "selected_client": client_filter,
    })


@workspace_required
def campaign_detail(request, pk):
    campaign = get_object_or_404(
        Campaign.objects.select_related("client"),
        pk=pk,
        client__workspace=request.workspace
    )
    content_items = campaign.content_items.all().select_related("creator").order_by("-created_at")
    metrics = campaign.metrics.all().order_by("-recorded_date")

    return render(request, "campaigns/detail.html", {
        "campaign": campaign,
        "content_items": content_items,
        "metrics": metrics,
    })


@workspace_required
@role_required([Membership.Role.ADMIN, Membership.Role.MANAGER])
def campaign_create(request):
    clients = Client.objects.filter(workspace=request.workspace)
    if not clients.exists():
        messages.warning(request, "Please add at least one client before creating a campaign.")
        return redirect("clients:create")

    if request.method == "POST":
        client_id = request.POST.get("client_id")
        title = request.POST.get("title", "").strip()
        objective = request.POST.get("objective", "").strip()
        target_audience = request.POST.get("target_audience", "").strip()
        status_val = request.POST.get("status", Campaign.Status.PLANNING)
        start_date = request.POST.get("start_date") or None
        end_date = request.POST.get("end_date") or None
        budget = request.POST.get("budget") or 0.00

        client = get_object_or_404(Client, id=client_id, workspace=request.workspace)

        if not title:
            messages.error(request, "Campaign title is required.")
        else:
            camp = Campaign.objects.create(
                client=client,
                title=title,
                objective=objective,
                target_audience=target_audience,
                status=status_val,
                start_date=start_date,
                end_date=end_date,
                budget=budget,
            )
            messages.success(request, f"Campaign '{camp.title}' created successfully.")
            return redirect("campaigns:detail", pk=camp.pk)

    return render(request, "campaigns/form.html", {
        "title": "Create Campaign",
        "clients": clients,
        "statuses": Campaign.Status.choices,
    })


@workspace_required
@role_required([Membership.Role.ADMIN, Membership.Role.MANAGER])
def campaign_update(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, client__workspace=request.workspace)
    clients = Client.objects.filter(workspace=request.workspace)

    if request.method == "POST":
        client_id = request.POST.get("client_id")
        campaign.client = get_object_or_404(Client, id=client_id, workspace=request.workspace)
        campaign.title = request.POST.get("title", "").strip() or campaign.title
        campaign.objective = request.POST.get("objective", "").strip()
        campaign.target_audience = request.POST.get("target_audience", "").strip()
        campaign.status = request.POST.get("status", campaign.status)
        campaign.start_date = request.POST.get("start_date") or None
        campaign.end_date = request.POST.get("end_date") or None
        campaign.budget = request.POST.get("budget") or campaign.budget
        campaign.save()

        messages.success(request, f"Campaign '{campaign.title}' updated.")
        return redirect("campaigns:detail", pk=campaign.pk)

    return render(request, "campaigns/form.html", {
        "title": f"Edit {campaign.title}",
        "campaign": campaign,
        "clients": clients,
        "statuses": Campaign.Status.choices,
    })


@workspace_required
@role_required([Membership.Role.ADMIN])
def campaign_delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, client__workspace=request.workspace)
    if request.method == "POST":
        title = campaign.title
        campaign.delete()
        messages.success(request, f"Campaign '{title}' deleted.")
        return redirect("campaigns:list")
    return render(request, "campaigns/confirm_delete.html", {"campaign": campaign})


# DRF API ViewSet
class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated, IsWorkspaceMember]

    def get_queryset(self):
        ws = getattr(self.request, "workspace", None)
        if ws:
            return Campaign.objects.filter(client__workspace=ws).select_related("client")
        return Campaign.objects.none()

    def perform_create(self, serializer):
        # Enforce that client belongs to user's active workspace
        client_id = self.request.data.get("client")
        client = get_object_or_404(Client, id=client_id, workspace=self.request.workspace)
        serializer.save(client=client)

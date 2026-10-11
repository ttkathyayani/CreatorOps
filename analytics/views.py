from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from workspaces.permissions import workspace_required, IsWorkspaceMember
from clients.models import Client
from campaigns.models import Campaign
from content.models import ContentItem
from approvals.models import Approval
from agents.content_ideas import ContentIdeasAgent
from agents.script_review import ScriptReviewAgent
from agents.approval_summary import ApprovalSummaryAgent
from agents.campaign_report import CampaignReportAgent
from .models import CampaignMetric


@workspace_required
def dashboard_view(request):
    ws = request.workspace

    clients = Client.objects.filter(workspace=ws)
    campaigns = Campaign.objects.filter(client__workspace=ws)
    content_items = ContentItem.objects.filter(campaign__client__workspace=ws)

    # Workflow counts
    counts = {
        "clients": clients.count(),
        "campaigns": campaigns.count(),
        "total_content": content_items.count(),
        "draft": content_items.filter(status=ContentItem.Status.DRAFT).count(),
        "pending_manager": content_items.filter(status=ContentItem.Status.PENDING_MANAGER).count(),
        "pending_client": content_items.filter(status=ContentItem.Status.PENDING_CLIENT).count(),
        "approved": content_items.filter(status=ContentItem.Status.APPROVED).count(),
        "changes_requested": content_items.filter(status=ContentItem.Status.CHANGES_REQUESTED).count(),
        "published": content_items.filter(status=ContentItem.Status.PUBLISHED).count(),
    }

    # Recent content items
    recent_items = content_items.select_related("campaign", "campaign__client", "creator")[:6]

    # Pending approvals for current user's role
    role = request.membership.role if request.membership else None
    pending_for_role = []
    if role == "MANAGER":
        pending_for_role = content_items.filter(status=ContentItem.Status.PENDING_MANAGER)[:5]
    elif role == "CLIENT_REVIEWER":
        pending_for_role = content_items.filter(status=ContentItem.Status.PENDING_CLIENT)[:5]
    else:
        pending_for_role = content_items.filter(
            status__in=[ContentItem.Status.PENDING_MANAGER, ContentItem.Status.PENDING_CLIENT]
        )[:5]

    return render(request, "dashboard/index.html", {
        "counts": counts,
        "recent_items": recent_items,
        "pending_for_role": pending_for_role,
        "campaigns": campaigns[:5],
    })


@workspace_required
def campaign_report_view(request, campaign_id):
    campaign = get_object_or_404(
        Campaign.objects.select_related("client"),
        pk=campaign_id,
        client__workspace=request.workspace
    )

    if request.method == "POST":
        metric_name = request.POST.get("metric_name", "").strip()
        metric_value = request.POST.get("metric_value", "").strip()
        recorded_date = request.POST.get("recorded_date")

        if metric_name and metric_value and recorded_date:
            try:
                CampaignMetric.objects.create(
                    campaign=campaign,
                    metric_name=metric_name,
                    metric_value=float(metric_value),
                    recorded_date=recorded_date,
                )
                messages.success(request, f"Metric '{metric_name}' recorded.")
            except ValueError:
                messages.error(request, "Invalid metric value.")
        return redirect("analytics:campaign_report", campaign_id=campaign.id)

    metrics = campaign.metrics.all()
    content_items = campaign.content_items.all()

    # Prepare data for CampaignReportAgent
    report_agent = CampaignReportAgent()
    agent_input = {
        "title": campaign.title,
        "client_name": campaign.client.name,
        "status": campaign.status,
        "budget": float(campaign.budget),
        "total_content": content_items.count(),
        "published_content": content_items.filter(status=ContentItem.Status.PUBLISHED).count(),
        "pending_content": content_items.filter(
            status__in=[ContentItem.Status.PENDING_MANAGER, ContentItem.Status.PENDING_CLIENT]
        ).count(),
        "metrics": [
            {"metric_name": m.metric_name, "metric_value": float(m.metric_value)}
            for m in metrics
        ],
    }

    ai_report = report_agent.run(agent_input)

    return render(request, "reports/campaign_report.html", {
        "campaign": campaign,
        "metrics": metrics,
        "content_items": content_items,
        "ai_report": ai_report,
    })


@workspace_required
def agent_workspace_view(request):
    """Interactive AI Agent studio for all 4 agents."""
    clients = Client.objects.filter(workspace=request.workspace)
    campaigns = Campaign.objects.filter(client__workspace=request.workspace)
    content_items = ContentItem.objects.filter(campaign__client__workspace=request.workspace)

    return render(request, "agents/workspace.html", {
        "clients": clients,
        "campaigns": campaigns,
        "content_items": content_items,
    })


# API Endpoints
class CampaignReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsWorkspaceMember]

    def get(self, request, pk):
        campaign = get_object_or_404(
            Campaign,
            pk=pk,
            client__workspace=request.workspace
        )
        metrics = campaign.metrics.all()
        content_items = campaign.content_items.all()

        agent = CampaignReportAgent()
        report = agent.run({
            "title": campaign.title,
            "client_name": campaign.client.name,
            "status": campaign.status,
            "budget": float(campaign.budget),
            "total_content": content_items.count(),
            "published_content": content_items.filter(status=ContentItem.Status.PUBLISHED).count(),
            "pending_content": content_items.filter(
                status__in=[ContentItem.Status.PENDING_MANAGER, ContentItem.Status.PENDING_CLIENT]
            ).count(),
            "metrics": [{"metric_name": m.metric_name, "metric_value": float(m.metric_value)} for m in metrics],
        })
        return Response(report)


from django.views.decorators.csrf import csrf_exempt

# AI Agent execution API
@csrf_exempt
def api_run_agent(request, agent_type):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    import json
    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST.dict()

    if agent_type == "content-ideas":
        res = ContentIdeasAgent().run(data)
    elif agent_type == "script-review":
        res = ScriptReviewAgent().run(data)
    elif agent_type == "approval-summary":
        res = ApprovalSummaryAgent().run(data)
    elif agent_type == "campaign-report":
        res = CampaignReportAgent().run(data)
    else:
        return JsonResponse({"error": f"Unknown agent: {agent_type}"}, status=400)

    return JsonResponse(res)

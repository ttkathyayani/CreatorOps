from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from workspaces.permissions import workspace_required, IsWorkspaceMember
from workspaces.models import Membership
from content.models import ContentItem
from .models import Approval
from .serializers import ApprovalSerializer


@workspace_required
def approval_queue(request):
    """
    Shows content items awaiting review relevant to user's role:
    - Manager: items in pending_manager
    - Client Reviewer: items in pending_client
    - Admin: all items in pending_manager or pending_client
    """
    role = request.membership.role

    items = ContentItem.objects.filter(
        campaign__client__workspace=request.workspace,
        status__in=[ContentItem.Status.PENDING_MANAGER, ContentItem.Status.PENDING_CLIENT]
    ).select_related("campaign", "campaign__client", "creator").order_by("due_date", "-updated_at")

    if role == Membership.Role.MANAGER:
        filtered_items = items.filter(status=ContentItem.Status.PENDING_MANAGER)
    elif role == Membership.Role.CLIENT_REVIEWER:
        filtered_items = items.filter(status=ContentItem.Status.PENDING_CLIENT)
    else:
        filtered_items = items

    return render(request, "approvals/queue.html", {
        "items": filtered_items,
        "all_items": items,
        "role": role,
    })


@workspace_required
def review_action(request, content_id):
    """
    Handles approving or requesting revisions on a content item.
    Enforces strict role permissions.
    """
    if request.method != "POST":
        return redirect("content:detail", pk=content_id)

    item = get_object_or_404(
        ContentItem,
        pk=content_id,
        campaign__client__workspace=request.workspace
    )
    role = request.membership.role
    decision = request.POST.get("decision")  # 'APPROVE' or 'REQUEST_CHANGES'
    comment = request.POST.get("comment", "").strip()

    if not comment:
        messages.error(request, "Please provide feedback or a review comment.")
        return redirect("content:detail", pk=content_id)

    # 1. Creator is strictly forbidden from approving
    if role == Membership.Role.CREATOR:
        messages.error(request, "Permission Denied: Creators cannot approve content.")
        raise PermissionDenied("Creators cannot perform review actions.")

    # 2. Manager Review step
    if item.status == ContentItem.Status.PENDING_MANAGER:
        if role not in [Membership.Role.MANAGER, Membership.Role.ADMIN]:
            messages.error(request, "Only Managers or Admins can review at this stage.")
            raise PermissionDenied("Only Managers can review pending_manager items.")

        if decision == "APPROVE":
            item.status = ContentItem.Status.PENDING_CLIENT
            approval_decision = Approval.Decision.MANAGER_APPROVED
            messages.success(request, f"Manager approved '{item.title}'. Advanced to Client Review.")
        else:
            item.status = ContentItem.Status.CHANGES_REQUESTED
            approval_decision = Approval.Decision.MANAGER_CHANGES_REQUESTED
            messages.warning(request, f"Changes requested on '{item.title}'. Returned to Creator.")

    # 3. Client Review step
    elif item.status == ContentItem.Status.PENDING_CLIENT:
        if role not in [Membership.Role.CLIENT_REVIEWER, Membership.Role.ADMIN]:
            messages.error(request, "Only Client Reviewers or Admins can review at this stage.")
            raise PermissionDenied("Only Client Reviewers can review pending_client items.")

        if decision == "APPROVE":
            item.status = ContentItem.Status.APPROVED
            approval_decision = Approval.Decision.CLIENT_APPROVED
            messages.success(request, f"Client approved '{item.title}'. Content is ready for scheduling/publishing!")
        else:
            item.status = ContentItem.Status.CHANGES_REQUESTED
            approval_decision = Approval.Decision.CLIENT_CHANGES_REQUESTED
            messages.warning(request, f"Client requested changes on '{item.title}'. Returned to Creator.")

    else:
        messages.error(request, f"Content is not currently pending review (current status: {item.get_status_display()}).")
        return redirect("content:detail", pk=content_id)

    item.save()

    # Record audit log
    Approval.objects.create(
        content_item=item,
        reviewer=request.user,
        decision=approval_decision,
        comment=comment,
    )

    return redirect("content:detail", pk=content_id)


# REST API Endpoint: POST /api/content/{id}/review/
class ContentReviewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsWorkspaceMember]

    def post(self, request, pk):
        item = get_object_or_404(
            ContentItem,
            pk=pk,
            campaign__client__workspace=request.workspace
        )
        membership = request.membership
        role = membership.role
        decision = request.data.get("decision")  # 'APPROVE' or 'REQUEST_CHANGES'
        comment = request.data.get("comment", "").strip()

        if not comment:
            return Response({"error": "Comment is required"}, status=status.HTTP_400_BAD_REQUEST)

        if role == Membership.Role.CREATOR:
            return Response({"error": "Creators cannot perform review actions"}, status=status.HTTP_403_FORBIDDEN)

        if item.status == ContentItem.Status.PENDING_MANAGER:
            if role not in [Membership.Role.MANAGER, Membership.Role.ADMIN]:
                return Response({"error": "Manager role required"}, status=status.HTTP_403_FORBIDDEN)
            if decision == "APPROVE":
                item.status = ContentItem.Status.PENDING_CLIENT
                app_dec = Approval.Decision.MANAGER_APPROVED
            else:
                item.status = ContentItem.Status.CHANGES_REQUESTED
                app_dec = Approval.Decision.MANAGER_CHANGES_REQUESTED

        elif item.status == ContentItem.Status.PENDING_CLIENT:
            if role not in [Membership.Role.CLIENT_REVIEWER, Membership.Role.ADMIN]:
                return Response({"error": "Client Reviewer role required"}, status=status.HTTP_403_FORBIDDEN)
            if decision == "APPROVE":
                item.status = ContentItem.Status.APPROVED
                app_dec = Approval.Decision.CLIENT_APPROVED
            else:
                item.status = ContentItem.Status.CHANGES_REQUESTED
                app_dec = Approval.Decision.CLIENT_CHANGES_REQUESTED
        else:
            return Response({"error": f"Invalid item state: {item.status}"}, status=status.HTTP_400_BAD_REQUEST)

        item.save()
        approval = Approval.objects.create(
            content_item=item,
            reviewer=request.user,
            decision=app_dec,
            comment=comment,
        )

        serializer = ApprovalSerializer(approval)
        return Response({
            "status": "success",
            "content_status": item.status,
            "approval": serializer.data,
        }, status=status.HTTP_201_CREATED)

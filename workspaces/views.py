from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Workspace, Membership
from .permissions import workspace_required, role_required, get_active_workspace, get_membership


@login_required
def switch_workspace(request, workspace_id):
    membership = Membership.objects.filter(user=request.user, workspace_id=workspace_id).first()
    if membership:
        request.session["active_workspace_id"] = workspace_id
        messages.success(request, f"Switched to workspace: {membership.workspace.name}")
    else:
        messages.error(request, "You are not a member of this workspace.")
    return redirect(request.META.get("HTTP_REFERER", "dashboard"))


@login_required
def quick_role_switch(request, role):
    """
    Direct role switching is disabled. Access is strictly determined by account authentication.
    """
    messages.error(request, "Direct role switching is disabled. Your role is determined by your user account. To switch roles, please logout and sign in as that user.")
    return redirect(request.META.get("HTTP_REFERER", "dashboard"))


@login_required
def create_workspace(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        if not name:
            messages.error(request, "Workspace name is required.")
        else:
            ws = Workspace.objects.create(name=name, description=description)
            Membership.objects.create(user=request.user, workspace=ws, role=Membership.Role.ADMIN)
            request.session["active_workspace_id"] = ws.id
            messages.success(request, f"Workspace '{ws.name}' created successfully.")
            return redirect("dashboard")
    return render(request, "workspaces/create.html")


@workspace_required
@role_required([Membership.Role.ADMIN])
def workspace_members(request):
    ws = request.workspace
    members = Membership.objects.filter(workspace=ws).select_related("user")

    if request.method == "POST":
        # Only ADMIN can invite or change roles
        if request.membership.role != Membership.Role.ADMIN:
            messages.error(request, "Only Agency Admins can manage workspace members.")
            return redirect("workspaces:members")

        action = request.POST.get("action")
        if action == "invite":
            email = request.POST.get("email", "").strip().lower()
            role = request.POST.get("role", Membership.Role.CREATOR)
            username = request.POST.get("username", "").strip() or email.split("@")[0]

            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email}
            )
            if created:
                user.set_password("pass123")
                user.save()

            membership, m_created = Membership.objects.get_or_create(
                user=user,
                workspace=ws,
                defaults={"role": role}
            )
            if not m_created:
                membership.role = role
                membership.save()
                messages.info(request, f"Updated role for {user.username} to {membership.get_role_display()}.")
            else:
                messages.success(request, f"Added {user.username} as {membership.get_role_display()}.")

        elif action == "update_role":
            member_id = request.POST.get("member_id")
            new_role = request.POST.get("new_role")
            target_mem = get_object_or_404(Membership, id=member_id, workspace=ws)
            if new_role in Membership.Role.values:
                target_mem.role = new_role
                target_mem.save()
                messages.success(request, f"Updated {target_mem.user.username}'s role to {target_mem.get_role_display()}.")

        return redirect("workspaces:members")

    return render(request, "workspaces/members.html", {
        "workspace": ws,
        "members": members,
        "roles": Membership.Role.choices,
    })

from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework import permissions
from .models import Membership, Workspace


def get_active_workspace(request):
    """Retrieve verified active workspace for the logged in user."""
    if not request.user.is_authenticated:
        return None
    ws_id = request.session.get("active_workspace_id")
    if ws_id:
        membership = Membership.objects.filter(user=request.user, workspace_id=ws_id).select_related("workspace").first()
        if membership:
            return membership.workspace
    first_membership = Membership.objects.filter(user=request.user).select_related("workspace").first()
    if first_membership:
        request.session["active_workspace_id"] = first_membership.workspace.id
        return first_membership.workspace
    return None


def get_membership(user, workspace):
    if not user.is_authenticated or not workspace:
        return None
    return Membership.objects.filter(user=user, workspace=workspace).first()


def workspace_required(view_func):
    """Ensures user is authenticated and belongs to an active workspace."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        ws = get_active_workspace(request)
        if not ws:
            messages.warning(request, "Please create or join a workspace to continue.")
            return redirect("workspaces:create")
        request.workspace = ws
        request.membership = get_membership(request.user, ws)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def role_required(allowed_roles):
    """Decorator checking if the user holds one of the specified roles in the active workspace."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("accounts:login")
            ws = get_active_workspace(request)
            if not ws:
                return redirect("workspaces:create")
            membership = get_membership(request.user, ws)
            if not membership or membership.role not in allowed_roles:
                messages.error(request, f"Permission Denied. Required role: {', '.join(allowed_roles)}")
                raise PermissionDenied("You do not have permission to perform this action.")
            request.workspace = ws
            request.membership = membership
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# DRF Permissions
class IsWorkspaceMember(permissions.BasePermission):
    """Allows access only to authenticated users who are members of the requested workspace."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        ws = get_active_workspace(request)
        if not ws:
            return False
        request.workspace = ws
        request.membership = get_membership(request.user, ws)
        return bool(request.membership)


class IsWorkspaceAdminOrManager(permissions.BasePermission):
    """Allows access to Admin or Manager roles in the active workspace."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        ws = get_active_workspace(request)
        if not ws:
            return False
        membership = get_membership(request.user, ws)
        return bool(membership and membership.role in [Membership.Role.ADMIN, Membership.Role.MANAGER])

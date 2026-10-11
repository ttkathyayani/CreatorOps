from .models import Workspace, Membership


def workspace_context(request):
    """
    Context processor providing active_workspace, user_role,
    and user_memberships across all templates.
    """
    if not request.user.is_authenticated:
        return {
            "active_workspace": None,
            "user_role": None,
            "user_role_label": None,
            "user_memberships": [],
        }

    memberships = Membership.objects.filter(user=request.user).select_related("workspace")

    # If the user has a selected workspace in session, verify membership
    active_ws_id = request.session.get("active_workspace_id")
    active_membership = None

    if active_ws_id:
        active_membership = memberships.filter(workspace_id=active_ws_id).first()

    # Fallback to the first available membership
    if not active_membership and memberships.exists():
        active_membership = memberships.first()
        request.session["active_workspace_id"] = active_membership.workspace.id

    if active_membership:
        return {
            "active_workspace": active_membership.workspace,
            "user_role": active_membership.role,
            "user_role_label": active_membership.get_role_display(),
            "user_memberships": memberships,
        }

    return {
        "active_workspace": None,
        "user_role": None,
        "user_role_label": None,
        "user_memberships": [],
    }

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from workspaces.models import Workspace, Membership


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Pick active workspace
            membership = Membership.objects.filter(user=user).first()
            if membership:
                request.session["active_workspace_id"] = membership.workspace.id
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        role = request.POST.get("role", Membership.Role.CREATOR)
        agency_name = request.POST.get("agency_name", "").strip()

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, "accounts/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, "accounts/register.html")

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)

        # Create or join workspace
        ws_name = agency_name or f"{username.title()}'s Agency"
        ws = Workspace.objects.create(name=ws_name)
        # First registrant of workspace gets ADMIN or chosen role
        actual_role = Membership.Role.ADMIN if agency_name else role
        Membership.objects.create(user=user, workspace=ws, role=actual_role)
        request.session["active_workspace_id"] = ws.id

        messages.success(request, f"Account created! Welcome to {ws.name}.")
        return redirect("dashboard")

    return render(request, "accounts/register.html", {
        "roles": Membership.Role.choices,
    })


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")

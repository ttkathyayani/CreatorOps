from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from workspaces.permissions import workspace_required, role_required, IsWorkspaceMember
from workspaces.models import Membership
from .models import Client
from .serializers import ClientSerializer


# Template Views
@workspace_required
def client_list(request):
    clients = Client.objects.filter(workspace=request.workspace).prefetch_related("campaigns")
    return render(request, "clients/list.html", {"clients": clients})


@workspace_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk, workspace=request.workspace)
    campaigns = client.campaigns.all().order_by("-created_at")
    return render(request, "clients/detail.html", {
        "client": client,
        "campaigns": campaigns,
    })


@workspace_required
@role_required([Membership.Role.ADMIN, Membership.Role.MANAGER])
def client_create(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        contact_email = request.POST.get("contact_email", "").strip()
        industry = request.POST.get("industry", "").strip()
        company_notes = request.POST.get("company_notes", "").strip()
        brand_guidelines = request.POST.get("brand_guidelines", "").strip()

        if not name:
            messages.error(request, "Client name is required.")
        else:
            client = Client.objects.create(
                workspace=request.workspace,
                name=name,
                contact_email=contact_email,
                industry=industry,
                company_notes=company_notes,
                brand_guidelines=brand_guidelines,
            )
            messages.success(request, f"Client '{client.name}' added successfully.")
            return redirect("clients:detail", pk=client.pk)

    return render(request, "clients/form.html", {"title": "Add New Client"})


@workspace_required
@role_required([Membership.Role.ADMIN, Membership.Role.MANAGER])
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk, workspace=request.workspace)
    if request.method == "POST":
        client.name = request.POST.get("name", "").strip() or client.name
        client.contact_email = request.POST.get("contact_email", "").strip()
        client.industry = request.POST.get("industry", "").strip()
        client.company_notes = request.POST.get("company_notes", "").strip()
        client.brand_guidelines = request.POST.get("brand_guidelines", "").strip()
        client.save()
        messages.success(request, f"Client '{client.name}' updated successfully.")
        return redirect("clients:detail", pk=client.pk)

    return render(request, "clients/form.html", {
        "title": f"Edit {client.name}",
        "client": client,
    })


@workspace_required
@role_required([Membership.Role.ADMIN])
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk, workspace=request.workspace)
    if request.method == "POST":
        name = client.name
        client.delete()
        messages.success(request, f"Client '{name}' removed.")
        return redirect("clients:list")
    return render(request, "clients/confirm_delete.html", {"client": client})


# REST API ViewSet
class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated, IsWorkspaceMember]

    def get_queryset(self):
        ws = getattr(self.request, "workspace", None)
        if ws:
            return Client.objects.filter(workspace=ws)
        return Client.objects.none()

    def perform_create(self, serializer):
        serializer.save(workspace=self.request.workspace)

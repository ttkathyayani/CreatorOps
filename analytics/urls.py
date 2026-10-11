from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("reports/campaigns/<int:campaign_id>/", views.campaign_report_view, name="campaign_report"),
    path("agents/", views.agent_workspace_view, name="agents"),
]

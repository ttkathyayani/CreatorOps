from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("reports/campaigns/<int:campaign_id>/", views.campaign_report_view, name="campaign_report"),
    path("agents/", views.agent_workspace_view, name="agents"),
    path("competitors/", views.competitors_view, name="competitors"),
    path("api/competitors/benchmark/", views.api_competitors_benchmark, name="api_competitors_benchmark"),
    path("api/competitors/", views.api_add_competitor, name="api_add_competitor"),
]


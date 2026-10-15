from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter

from clients.views import ClientViewSet
from campaigns.views import CampaignViewSet
from content.views import ContentItemViewSet, api_script_review
from approvals.views import ContentReviewAPIView
from analytics.views import dashboard_view, CampaignReportAPIView, api_run_agent

# DRF Router for standard REST APIs
router = DefaultRouter()
router.register(r"clients", ClientViewSet, basename="api-clients")
router.register(r"campaigns", CampaignViewSet, basename="api-campaigns")
router.register(r"content", ContentItemViewSet, basename="api-content")

from django.http import HttpResponse

def review_guide_view(request):
    guide_path = settings.BASE_DIR / "CREATOROPS_PROJECT_MASTER_REVIEW_GUIDE.html"
    if guide_path.exists():
        with open(guide_path, "r", encoding="utf-8") as f:
            return HttpResponse(f.read(), content_type="text/html")
    return HttpResponse("Guide not found", status=404)

def review2_report_view(request):
    report_path = settings.BASE_DIR / "REVIEW_2_REPORT.html"
    if report_path.exists():
        with open(report_path, "r", encoding="utf-8") as f:
            return HttpResponse(f.read(), content_type="text/html")
    return HttpResponse("Review 2 Report not found", status=404)

def review2_download_view(request):
    md_path = settings.BASE_DIR / "REVIEW_2_REPORT.md"
    if md_path.exists():
        with open(md_path, "r", encoding="utf-8") as f:
            response = HttpResponse(f.read(), content_type="text/markdown; charset=utf-8")
            response["Content-Disposition"] = 'attachment; filename="REVIEW_2_REPORT_CreatorOps.md"'
            return response
    return HttpResponse("Markdown file not found", status=404)

def review3_report_view(request):
    report_path = settings.BASE_DIR / "REVIEW_3_FINAL_REPORT.html"
    if report_path.exists():
        with open(report_path, "r", encoding="utf-8") as f:
            return HttpResponse(f.read(), content_type="text/html")
    return HttpResponse("Review 3 Final Report not found", status=404)

def review3_download_view(request):
    md_path = settings.BASE_DIR / "REVIEW_3_FINAL_REPORT.md"
    if md_path.exists():
        with open(md_path, "r", encoding="utf-8") as f:
            response = HttpResponse(f.read(), content_type="text/markdown; charset=utf-8")
            response["Content-Disposition"] = 'attachment; filename="REVIEW_3_FINAL_REPORT_CreatorOps.md"'
            return response
    return HttpResponse("Markdown file not found", status=404)

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("accounts:login")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", root_redirect, name="root"),
    path("guide/", review_guide_view, name="review-guide"),
    path("reports/review2/", review2_report_view, name="report-review2"),
    path("reports/review2/download/", review2_download_view, name="report-review2-download"),
    path("reports/review3/", review3_report_view, name="report-review3"),
    path("reports/review3/download/", review3_download_view, name="report-review3-download"),
    path("dashboard/", dashboard_view, name="dashboard"),

    # Application URLs (HTML Templates)
    path("accounts/", include("accounts.urls")),
    path("workspaces/", include("workspaces.urls")),
    path("clients/", include("clients.urls")),
    path("campaigns/", include("campaigns.urls")),
    path("content/", include("content.urls")),
    path("approvals/", include("approvals.urls")),
    path("assets/", include("assets.urls")),
    path("analytics/", include("analytics.urls")),

    # REST APIs (As specified in Course Project Guide Section 10)
    path("api/", include(router.urls)),
    path("api/content/<int:pk>/review/", ContentReviewAPIView.as_view(), name="api-content-review"),
    path("api/reports/campaigns/<int:pk>/", CampaignReportAPIView.as_view(), name="api-campaign-report"),
    path("api/agents/script-review/", api_script_review, name="api-script-review"),
    path("api/agents/<str:agent_type>/", api_run_agent, name="api-run-agent"),
]

from django.views.static import serve
from django.urls import re_path

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
elif not settings.USE_S3:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]

from django.urls import path
from . import views

app_name = "approvals"

urlpatterns = [
    path("queue/", views.approval_queue, name="queue"),
    path("review/<int:content_id>/", views.review_action, name="review"),
]

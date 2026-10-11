from django.urls import path
from . import views

app_name = "content"

urlpatterns = [
    path("", views.content_list, name="list"),
    path("calendar/", views.calendar_view, name="calendar"),
    path("create/", views.content_create, name="create"),
    path("<int:pk>/", views.content_detail, name="detail"),
    path("<int:pk>/edit/", views.content_edit, name="edit"),
    path("<int:pk>/submit/", views.submit_for_review, name="submit"),
    path("<int:pk>/publish/", views.publish_content, name="publish"),
]

from django.urls import path
from . import views

app_name = "workspaces"

urlpatterns = [
    path("create/", views.create_workspace, name="create"),
    path("switch/<int:workspace_id>/", views.switch_workspace, name="switch"),
    path("quick-role/<str:role>/", views.quick_role_switch, name="quick_role"),
    path("members/", views.workspace_members, name="members"),
]

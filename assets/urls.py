from django.urls import path
from . import views

app_name = "assets"

urlpatterns = [
    path("upload/<int:content_id>/", views.upload_asset, name="upload"),
    path("<int:pk>/download/", views.download_asset, name="download"),
    path("<int:pk>/delete/", views.delete_asset, name="delete"),
]

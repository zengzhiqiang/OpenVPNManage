from django.urls import path

from . import views

app_name = "OpenVPNApp"

urlpatterns = [
    path(r"", views.index, name="index"),
    path("restart", views.restart, name="restart"),
    path("downloadConfigFile", views.download_config_file, name="downloadConfigFile"),
    path("changePort", views.change_port, name="changePort"),
    path("start", views.start, name="start")
]
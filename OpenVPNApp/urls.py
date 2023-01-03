from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(r"/restart", views.restart, name="restart"),
    path(r"/downloadConfigFile", views.download_config_file, name="downloadConfigFile"),
    path(r"/changePort", views.change_port, name="changePort"),
    path(r"/start", views.start, name="start"),
]
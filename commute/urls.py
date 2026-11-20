from django.urls import path

from . import views

app_name = "commute"

urlpatterns = [
    path("", views.device_list, name="devices"),
    path("about/", views.about, name="about"),
    path("devices/", views.device_list, name="device_list"),
    path("devices/<int:device_id>/", views.device_detail, name="device_detail"),
    path("innovation/", views.innovation, name="innovation"),
    path("contact/", views.contact, name="contact"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("plan/", views.journey_planner, name="journey_planner"),
    path("traffic/", views.traffic, name="traffic"),
    path("transport/", views.transport, name="transport"),
    path("history/", views.journey_history, name="history"),
]

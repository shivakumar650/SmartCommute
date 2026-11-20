from django.urls import path

from . import views

app_name = "commute"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("plan/", views.journey_planner, name="journey_planner"),
    path("traffic/", views.traffic, name="traffic"),
    path("transport/", views.transport, name="transport"),
    path("history/", views.journey_history, name="history"),
]

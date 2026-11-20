from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import JourneyHistory, Route, Traffic, Transport


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        "route_name",
        "source",
        "destination",
        "distance_km",
        "base_travel_time",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("route_name", "source", "destination")


@admin.register(Traffic)
class TrafficAdmin(admin.ModelAdmin):
    list_display = ("route", "traffic_level", "delay_minutes", "updated_at")
    list_filter = ("traffic_level",)
    search_fields = ("route__route_name", "route__source", "route__destination")


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = (
        "route",
        "transport_type",
        "departure_time",
        "approximate_fare",
        "estimated_duration",
    )
    list_filter = ("transport_type",)
    search_fields = ("route__route_name", "route__source", "route__destination")


@admin.register(JourneyHistory)
class JourneyHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "source",
        "destination",
        "transport_type",
        "recommended_route",
        "estimated_travel_time",
        "searched_at",
    )
    list_filter = ("transport_type", "searched_at")
    search_fields = ("user__username", "source", "destination")

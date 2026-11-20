from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm, JourneyPlannerForm
from .models import (
    ContactMessage,
    Innovation,
    JourneyHistory,
    Route,
    SmartDevice,
    Traffic,
    Transport,
)
from .recommender import rank_routes


@login_required
def dashboard(request):
    journeys = JourneyHistory.objects.filter(user=request.user)
    recent_journeys = journeys.select_related(
        "recommended_route"
    )[:5]

    traffic_records = Traffic.objects.select_related("route")
    traffic_summary = {
        level: traffic_records.filter(traffic_level=level).count()
        for level in ("Low", "Moderate", "Heavy")
    }

    context = {
        "total_journeys": journeys.count(),
        "available_routes": Route.objects.filter(is_active=True).count(),
        "recent_journeys": recent_journeys,
        "traffic_summary": traffic_summary,
        "transport_types": sorted(
            Transport.objects.exclude(
                transport_type=""
            ).values_list("transport_type", flat=True).distinct()
        ),
    }
    return render(request, "dashboard.html", context)


@login_required
def journey_planner(request):
    form = JourneyPlannerForm(request.POST or None)
    context = {
        "form": form,
        "matching_routes": [],
        "ranked_routes": [],
        "search_performed": False,
    }

    if request.method == "POST" and form.is_valid():
        source = form.cleaned_data["source"]
        destination = form.cleaned_data["destination"]
        transport_type = form.cleaned_data["transport_type"]

        routes = Route.objects.filter(
            is_active=True,
            source__iexact=source,
            destination__iexact=destination,
        ).prefetch_related("traffic_records")

        matching_routes = [
            route for route in routes
            if route.supports_transport(transport_type)
        ]
        ranked_routes = rank_routes(matching_routes, transport_type)

        recommended = ranked_routes[0] if ranked_routes else None
        if recommended:
            JourneyHistory.objects.create(
                user=request.user,
                source=source,
                destination=destination,
                transport_type=transport_type,
                recommended_route=recommended["route"],
                estimated_travel_time=recommended["total_travel_time"],
            )

        context.update({
            "matching_routes": matching_routes,
            "ranked_routes": ranked_routes,
            "recommended": recommended,
            "search_performed": True,
            "search_source": source,
            "search_destination": destination,
            "search_transport": transport_type,
            "departure_time": form.cleaned_data["departure_time"],
        })

    return render(request, "journey_planner.html", context)


@login_required
def traffic(request):
    traffic_records = Traffic.objects.select_related("route").filter(
        route__is_active=True
    )
    return render(
        request,
        "traffic.html",
        {"traffic_records": traffic_records},
    )


@login_required
def transport(request):
    transport_records = Transport.objects.select_related("route").filter(
        route__is_active=True
    )
    return render(
        request,
        "transport.html",
        {"transport_records": transport_records},
    )


@login_required
def journey_history(request):
    journeys = JourneyHistory.objects.filter(
        user=request.user
    ).select_related("recommended_route")
    return render(
        request,
        "history.html",
        {"journeys": journeys},
    )


def about(request):
    return render(request, "about.html")


def home(request):
    featured_devices = SmartDevice.objects.filter(
        is_active=True
    )[:3]
    innovations = Innovation.objects.filter(is_active=True)[:3]
    return render(
        request,
        "home.html",
        {
            "featured_devices": featured_devices,
            "innovations": innovations,
        },
    )


def device_list(request):
    devices = SmartDevice.objects.filter(is_active=True)
    return render(request, "devices.html", {"devices": devices})


def device_detail(request, device_id):
    device = get_object_or_404(SmartDevice, id=device_id, is_active=True)
    return render(request, "device_detail.html", {"device": device})


def innovation(request):
    innovations = Innovation.objects.filter(is_active=True)
    return render(
        request,
        "innovation.html",
        {"innovations": innovations},
    )


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        ContactMessage.objects.create(**form.cleaned_data)
        messages.success(
            request,
            "Thank you. Your inquiry was submitted successfully.",
        )
        return redirect("commute:contact")
    return render(request, "contact.html", {"form": form})

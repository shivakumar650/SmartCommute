from django.db import models

# Create your models here.
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Route(models.Model):
    TRANSPORT_CHOICES = (
        ("Bus", "Bus"),
        ("Car", "Car"),
        ("Bike", "Bike"),
    )

    route_name = models.CharField(max_length=120)
    source = models.CharField(max_length=120)
    destination = models.CharField(max_length=120)
    distance_km = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0.1)]
    )
    base_travel_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    supported_transport_types = models.CharField(
        max_length=30,
        help_text="Comma-separated values: Bus, Car, Bike",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["route_name"]

    def __str__(self):
        return f"{self.route_name} ({self.source} - {self.destination})"

    def supports_transport(self, transport_type):
        supported = {
            value.strip()
            for value in self.supported_transport_types.split(",")
        }
        return transport_type in supported


class Traffic(models.Model):
    TRAFFIC_CHOICES = (
        ("Low", "Low Traffic"),
        ("Moderate", "Moderate Traffic"),
        ("Heavy", "Heavy Traffic"),
    )

    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="traffic_records"
    )
    traffic_level = models.CharField(
        max_length=10, choices=TRAFFIC_CHOICES, default="Low"
    )
    delay_minutes = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.route.route_name}: {self.get_traffic_level_display()}"


class Transport(models.Model):
    TRANSPORT_CHOICES = (
        ("Bus", "Bus"),
        ("Car", "Car"),
        ("Bike", "Bike"),
    )

    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="transport_options"
    )
    transport_type = models.CharField(max_length=10, choices=TRANSPORT_CHOICES)
    departure_time = models.TimeField()
    approximate_fare = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    estimated_duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ["departure_time", "transport_type"]

    def __str__(self):
        return f"{self.transport_type} - {self.route.route_name}"


class JourneyHistory(models.Model):
    TRANSPORT_CHOICES = (
        ("Bus", "Bus"),
        ("Car", "Car"),
        ("Bike", "Bike"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="journeys",
    )
    source = models.CharField(max_length=120)
    destination = models.CharField(max_length=120)
    transport_type = models.CharField(max_length=10, choices=TRANSPORT_CHOICES)
    recommended_route = models.ForeignKey(
        Route,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recommended_journeys",
    )
    estimated_travel_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-searched_at"]

    def __str__(self):
        return f"{self.user.username}: {self.source} to {self.destination}"

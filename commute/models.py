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


class SmartDevice(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to="devices/", blank=True)
    image_url = models.URLField(blank=True)
    description = models.TextField()
    features = models.TextField(
        help_text="Enter one feature per line."
    )
    working_principle = models.TextField()
    benefits = models.TextField()
    specifications = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def feature_list(self):
        return [item.strip() for item in self.features.splitlines() if item.strip()]


class Innovation(models.Model):
    title = models.CharField(max_length=120)
    summary = models.TextField()
    description = models.TextField()
    benefits = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=180)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.name}: {self.subject}"

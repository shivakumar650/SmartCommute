from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import JourneyHistory, Route, Traffic, Transport
from .recommender import rank_routes


class SmartCommuteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="commuter",
            password="SmartCommute-123",
        )
        self.other_user = User.objects.create_user(
            username="other",
            password="SmartCommute-123",
        )
        self.route = Route.objects.create(
            route_name="Green Park Express",
            source="Central Station",
            destination="Green Park",
            distance_km=8.5,
            base_travel_time=18,
            supported_transport_types="Bus,Car,Bike",
        )
        Traffic.objects.create(
            route=self.route,
            traffic_level="Low",
            delay_minutes=3,
        )
        Transport.objects.create(
            route=self.route,
            transport_type="Bus",
            departure_time="08:30",
            approximate_fare=12,
            estimated_duration=21,
        )
        self.client.login(username="commuter", password="SmartCommute-123")

    def test_dashboard_requires_authentication(self):
        self.client.logout()
        response = self.client.get(reverse("commute:dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_successful_journey_search_saves_history_and_recommends_route(self):
        response = self.client.post(reverse("commute:journey_planner"), {
            "source": "Central Station",
            "destination": "Green Park",
            "transport_type": "Bus",
            "departure_time": "08:30",
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["ranked_routes"]), 1)
        self.assertEqual(
            response.context["recommended"]["total_travel_time"],
            21,
        )
        journey = JourneyHistory.objects.get(user=self.user)
        self.assertEqual(journey.recommended_route, self.route)

    def test_search_with_no_matching_routes_is_empty(self):
        response = self.client.post(reverse("commute:journey_planner"), {
            "source": "Unknown",
            "destination": "Nowhere",
            "transport_type": "Bike",
            "departure_time": "09:00",
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["ranked_routes"], [])

    def test_recommender_uses_total_time_and_ranks_fastest_first(self):
        second_route = Route.objects.create(
            route_name="Fast Alternative",
            source="Central Station",
            destination="Green Park",
            distance_km=9,
            base_travel_time=15,
            supported_transport_types="Bus",
        )
        Traffic.objects.create(
            route=second_route,
            traffic_level="Heavy",
            delay_minutes=10,
        )

        ranked = rank_routes([self.route, second_route], "Bus")

        self.assertEqual(ranked[0]["route"], self.route)
        self.assertEqual(ranked[0]["total_travel_time"], 21)
        self.assertTrue(ranked[0]["is_recommended"])

    def test_traffic_and_transport_pages_show_database_records(self):
        traffic_response = self.client.get(reverse("commute:traffic"))
        transport_response = self.client.get(reverse("commute:transport"))

        self.assertEqual(traffic_response.status_code, 200)
        self.assertContains(traffic_response, "Low Traffic")
        self.assertEqual(transport_response.status_code, 200)
        self.assertContains(transport_response, "Green Park Express")

    def test_journey_history_is_user_specific(self):
        own = JourneyHistory.objects.create(
            user=self.user,
            source="Central Station",
            destination="Green Park",
            transport_type="Bus",
            recommended_route=self.route,
            estimated_travel_time=21,
        )
        JourneyHistory.objects.create(
            user=self.other_user,
            source="Central Market",
            destination="Old Town",
            transport_type="Bike",
            recommended_route=self.route,
            estimated_travel_time=30,
        )

        response = self.client.get(reverse("commute:history"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["journeys"]), [own])

    def test_dashboard_statistics_use_database_counts(self):
        JourneyHistory.objects.create(
            user=self.user,
            source="Central Station",
            destination="Green Park",
            transport_type="Bus",
            recommended_route=self.route,
            estimated_travel_time=21,
        )

        response = self.client.get(reverse("commute:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["available_routes"], 1)
        self.assertEqual(response.context["total_journeys"], 1)

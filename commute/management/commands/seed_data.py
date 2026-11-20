from django.core.management.base import BaseCommand

from commute.models import Route, Traffic, Transport


class Command(BaseCommand):
    help = "Populate SmartCommute with demonstration routes and transport data"

    def handle(self, *args, **options):
        Route.objects.all().delete()

        routes = [
            ("Green Park Express", "Central Station", "Green Park", 8.5, 18, "Bus,Car,Bike"),
            ("Lakeview Connector", "Central Station", "Lakeview Campus", 11.2, 24, "Bus,Car"),
            ("Tech City Route", "Central Station", "Tech City", 14.8, 30, "Bus,Car,Bike"),
            ("Old Town Shortcut", "Central Market", "Old Town", 6.3, 14, "Bike,Car"),
            ("Northside Line", "Central Market", "Northside Colony", 9.7, 21, "Bus,Bike"),
            ("Airport Road", "Green Park", "City Airport", 21.5, 38, "Bus,Car"),
            ("University Avenue", "Lakeview Campus", "University College", 7.4, 16, "Bus,Car,Bike"),
            ("River Bridge", "Old Town", "Riverside", 12.6, 26, "Bus,Car,Bike"),
            ("Industrial Ring", "Tech City", "Industrial Area", 15.9, 33, "Bus,Car"),
            ("South Central", "Northside Colony", "Central Station", 10.1, 22, "Bus,Car,Bike"),
        ]

        traffic_levels = [
            ("Low", 3),
            ("Moderate", 8),
            ("Heavy", 15),
            ("Low", 4),
            ("Moderate", 10),
            ("Heavy", 18),
            ("Low", 5),
            ("Moderate", 9),
            ("Heavy", 16),
            ("Moderate", 7),
        ]

        departures = {
            "Bus": ["07:30", "08:15", "09:00", "17:30", "18:15"],
            "Car": ["07:00", "08:00", "10:00", "16:30", "18:00"],
            "Bike": ["06:45", "07:45", "09:30", "16:00", "17:45"],
        }

        route_objects = []
        for index, (name, source, destination, distance, base_time, transports) in enumerate(routes):
            route = Route.objects.create(
                route_name=name,
                source=source,
                destination=destination,
                distance_km=distance,
                base_travel_time=base_time,
                supported_transport_types=transports,
                is_active=True,
            )
            route_objects.append(route)

            level, delay = traffic_levels[index]
            Traffic.objects.create(
                route=route,
                traffic_level=level,
                delay_minutes=delay,
            )

            supported = [value.strip() for value in transports.split(",")]
            for transport_type in supported:
                for position, departure in enumerate(departures[transport_type][:3]):
                    hour, minute = departure.split(":")
                    fare = (
                        round(float(distance) * (1.2 if transport_type == "Bus" else 2.8), 2)
                        if transport_type != "Bike"
                        else 15.00
                    )
                    transport_duration = base_time + traffic_levels[index][1] + position * 2
                    Transport.objects.create(
                        route=route,
                        transport_type=transport_type,
                        departure_time=f"{hour}:{minute}",
                        approximate_fare=fare,
                        estimated_duration=transport_duration,
                    )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(route_objects)} routes, traffic records, and transport schedules."
        ))

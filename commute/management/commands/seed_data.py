from django.core.management.base import BaseCommand

from commute.models import Innovation, Route, SmartDevice, Traffic, Transport


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

        SmartDevice.objects.get_or_create(
            name="Smart Bus Information Display",
            defaults={
                "description": "A connected information display that helps passengers see arrival information and available routes.",
                "features": "Real-time route display\nAccessible passenger information\nWeather-resistant enclosure",
                "working_principle": "The display receives route information and presents it to passengers at stops and terminals.",
                "benefits": "Reduces waiting uncertainty and helps passengers choose suitable routes.",
                "specifications": "Public display, digital route interface, network-ready design",
                "image_url": "https://images.unsplash.com/photo-1494526585095-c41746248156",
            },
        )
        SmartDevice.objects.get_or_create(
            name="Smart Helmet System",
            defaults={
                "description": "A conceptual wearable commuting device that improves rider awareness and safety.",
                "features": "Turn indicators\nHelmet communication\nEnhanced visibility",
                "working_principle": "The helmet uses visible indicators and communication tools to help riders remain aware of surroundings.",
                "benefits": "Improves rider visibility and communication.",
                "specifications": "Wearable concept, rechargeable indicator system",
            },
        )
        SmartDevice.objects.get_or_create(
            name="Smart Parking Assistant",
            defaults={
                "description": "An information system that helps drivers locate suitable parking spaces.",
                "features": "Parking status display\nGuidance indicators\nCapacity information",
                "working_principle": "Parking status is collected and shown through a simple display or website.",
                "benefits": "Reduces unnecessary vehicle circulation and saves time.",
                "specifications": "Digital parking display, status management interface",
            },
        )

        Innovation.objects.get_or_create(
            title="Unified Public Transport Guidance",
            defaults={
                "summary": "One understandable display system for buses, routes and travel guidance.",
                "description": "A central information platform can combine stops, schedules and route options for commuters.",
                "benefits": "Improves accessibility, reduces confusion and supports informed journey decisions.",
            },
        )
        Innovation.objects.get_or_create(
            title="Safer Bicycle Corridors",
            defaults={
                "summary": "Protected bicycle lanes with clear digital and physical guidance.",
                "description": "The concept uses dedicated lanes, visible signals and regular information points.",
                "benefits": "Encourages cycling and improves safety for riders.",
            },
        )

        self.stdout.write(self.style.SUCCESS(
            "Seeded smart devices and innovation records."
        ))

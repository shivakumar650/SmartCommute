def rank_routes(routes, transport_type):
    """Rank suitable routes using base time plus the latest traffic delay."""
    ranked_routes = []

    for route in routes:
        if not route.supports_transport(transport_type):
            continue

        traffic = route.traffic_records.first()
        traffic_level = traffic.get_traffic_level_display() if traffic else "No data"
        traffic_delay = traffic.delay_minutes if traffic else 0
        total_time = route.base_travel_time + traffic_delay

        ranked_routes.append({
            "route": route,
            "traffic_level": traffic_level,
            "traffic_delay": traffic_delay,
            "base_travel_time": route.base_travel_time,
            "total_travel_time": total_time,
            "distance_km": route.distance_km,
            "transport_type": transport_type,
        })

    ranked_routes.sort(
        key=lambda item: (
            item["total_travel_time"],
            item["distance_km"],
        )
    )

    for index, item in enumerate(ranked_routes):
        item["is_recommended"] = index == 0
        item["recommendation_status"] = (
            "Recommended" if index == 0 else "Alternative"
        )

    return ranked_routes

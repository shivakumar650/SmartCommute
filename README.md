# SmartCommute - Intelligent Commuting Management System

SmartCommute is a Django web application for planning journeys, comparing routes, viewing demonstration traffic conditions, reviewing transport schedules, and receiving rule-based route recommendations.

This is a software-only college project. The application does not use live traffic APIs, GPS, hardware, sensors, or external services.

## Features

- Registration, login, logout, and Django session authentication
- Authenticated dashboard with database-calculated statistics
- Journey planning and route matching
- Rule-based route ranking
- Demonstration traffic monitoring
- Bus, car, and bike transport schedules
- User-specific journey history
- Django Admin management
- Chart.js dashboard visualization

## Technology

- Python 3.12
- Django 6
- SQLite
- Django templates
- Bootstrap 5
- JavaScript
- Chart.js

## Setup

```powershell
cd "C:\Users\Shiva Kumar\OneDrive\Desktop\django_project"
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Admin

Create an administrator:

```powershell
python manage.py createsuperuser
```

Open `http://127.0.0.1:8000/admin/`.

The administrator can manage routes, traffic records, transport schedules, and journey history.

## Tests

```powershell
python manage.py test accounts commute
python manage.py check
```

## Project Structure

```text
accounts/       Authentication and account forms
commute/        Routes, traffic, transport, history, recommender
analytics/      Analytics app structure
templates/      Django HTML templates
static/         CSS and JavaScript
smartcommute/   Django project settings and URLs
manage.py       Django command entry point
db.sqlite3      SQLite database
```

## Database Design

### Route

- `route_name`
- `source`
- `destination`
- `distance_km`
- `base_travel_time`
- `supported_transport_types`
- `is_active`

### Traffic

- `route` foreign key
- `traffic_level`
- `delay_minutes`
- `updated_at`

### Transport

- `route` foreign key
- `transport_type`
- `departure_time`
- `approximate_fare`
- `estimated_duration`

### JourneyHistory

- `user` foreign key to Django User
- `source`
- `destination`
- `transport_type`
- `recommended_route` nullable foreign key
- `estimated_travel_time`
- `searched_at`

The ER relationship is: User -> JourneyHistory -> Route <- Traffic and Transport.

## Recommendation Formula

```text
Estimated Travel Time = Base Travel Time + Traffic Delay
```

The reusable implementation is in [commute/recommender.py](commute/recommender.py). Routes supporting the selected transport are ranked by estimated total time. The shortest suitable route is recommended.

## Traffic Data Notice

All traffic categories and delays are demonstration values stored in SQLite. They are not live measurements.

## Project Overview

SmartCommute helps students and commuters compare fictional sample routes and select a suitable route using transparent rule-based calculations.

## Problem Statement

Commuters need an understandable way to compare route alternatives, traffic conditions, transport options, and estimated travel times.

## Objectives

- Provide secure session-based user access
- Store routes and commuting records in SQLite
- Compare routes using deterministic rules
- Present meaningful route recommendations
- Preserve user-specific search history
- Provide a polished and responsive interface

## Software and Hardware Requirements

### Software

- Windows or another desktop operating system
- Python 3.12 or compatible supported version
- Django 6
- SQLite
- Modern web browser

### Hardware

No physical hardware is required. The project runs on a normal laptop or desktop computer.

## Functional Requirements

- Real registration and login
- CSRF-protected logout
- Authenticated dashboard and user pages
- Journey validation and route searches
- User-specific history
- Django Admin management
- Empty-result and error handling

## Testing Documentation

The test suite verifies:

- Registration
- Valid and invalid login
- Logout
- Protected dashboard access
- Successful route search
- Empty route search
- Recommendation ranking
- Traffic and transport displays
- Journey history privacy
- Database-calculated dashboard statistics

Run:

```powershell
python manage.py test accounts commute
```

## Screenshot Checklist

1. Home page
2. Registration form
3. Login form
4. Dashboard
5. Dashboard traffic chart
6. Journey planner form
7. Recommended route result
8. Alternative route comparison
9. No-result message
10. Traffic information
11. Transport information
12. Journey history
13. Django Admin route list
14. Django Admin traffic list
15. Django Admin transport list

## Future Enhancements

- Live data integration with authorized providers
- Route map visualization
- Departure-time-aware traffic schedules
- Email notifications
- Mobile application
- Advanced route preferences

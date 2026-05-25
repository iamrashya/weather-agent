"""Weather Agent — fetches real-time weather for the top 10 most populous
countries and major Indian metro cities using the free Open-Meteo API
(no API key required). Displays a formatted table in the terminal and
exposes get_weather_data() for reuse by app.py / scheduler.py.
"""

from datetime import datetime

import requests
from tabulate import tabulate


# Top 10 countries + major Indian metro cities.
LOCATIONS = [
    {"country": "China",      "capital": "Beijing",       "lat": 39.9042,  "lon": 116.4074},
    {"country": "India",      "capital": "New Delhi",     "lat": 28.6139,  "lon": 77.2090},
    {"country": "USA",        "capital": "Washington DC", "lat": 38.9072,  "lon": -77.0369},
    {"country": "Indonesia",  "capital": "Jakarta",       "lat": -6.2088,  "lon": 106.8456},
    {"country": "Pakistan",   "capital": "Islamabad",     "lat": 33.6844,  "lon": 73.0479},
    {"country": "Brazil",     "capital": "Brasilia",      "lat": -15.7942, "lon": -47.8822},
    {"country": "Nigeria",    "capital": "Abuja",         "lat": 9.0765,   "lon": 7.3986},
    {"country": "Bangladesh", "capital": "Dhaka",         "lat": 23.8103,  "lon": 90.4125},
    {"country": "Russia",     "capital": "Moscow",        "lat": 55.7558,  "lon": 37.6173},
    {"country": "Ethiopia",   "capital": "Addis Ababa",   "lat": 9.0320,   "lon": 38.7469},
    {"country": "India",      "capital": "Mumbai",        "lat": 19.0760,  "lon": 72.8777},
    {"country": "India",      "capital": "Delhi",         "lat": 28.7041,  "lon": 77.1025},
    {"country": "India",      "capital": "Bangalore",     "lat": 12.9716,  "lon": 77.5946},
    {"country": "India",      "capital": "Chennai",       "lat": 13.0827,  "lon": 80.2707},
    {"country": "India",      "capital": "Kolkata",       "lat": 22.5726,  "lon": 88.3639},
    {"country": "India",      "capital": "Hyderabad",     "lat": 17.3850,  "lon": 78.4867},
    {"country": "India",      "capital": "Pune",          "lat": 18.5204,  "lon": 73.8567},
    {"country": "India",      "capital": "Ahmedabad",     "lat": 23.0225,  "lon": 72.5714},
]

WEATHER_CODES = {
    0:  "Clear Sky",
    1:  "Mainly Clear",
    2:  "Partly Cloudy",
    3:  "Overcast",
    45: "Foggy",
    48: "Icy Fog",
    51: "Light Drizzle",
    53: "Drizzle",
    55: "Heavy Drizzle",
    61: "Slight Rain",
    63: "Rain",
    65: "Heavy Rain",
    71: "Slight Snow",
    73: "Snow",
    75: "Heavy Snow",
    80: "Rain Showers",
    81: "Heavy Rain Showers",
    95: "Thunderstorm",
    99: "Thunderstorm with Hail",
}

API_URL = "https://api.open-meteo.com/v1/forecast"

TABLE_HEADERS = [
    "Rank", "Country/City", "Capital/City", "Temp (°C)",
    "Wind (km/h)", "Humidity (%)", "Rainfall (mm)", "Condition",
]


def fetch_weather(lat: float, lon: float) -> dict:
    """Call Open-Meteo and return current weather plus first hourly humidity/precip."""
    response = requests.get(
        API_URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true",
            "hourly": "relativehumidity_2m,precipitation",
            "forecast_days": 1,
            "timezone": "auto",
        },
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()
    current = data.get("current_weather", {}) or {}
    hourly = data.get("hourly", {}) or {}
    humidity_list = hourly.get("relativehumidity_2m") or []
    precip_list = hourly.get("precipitation") or []
    return {
        "temperature": current.get("temperature"),
        "windspeed": current.get("windspeed"),
        "weathercode": current.get("weathercode"),
        "humidity": humidity_list[0] if humidity_list else None,
        "rainfall": precip_list[0] if precip_list else None,
    }


def _fallback(value, default="N/A"):
    return value if value is not None else default


def get_weather_data() -> list:
    """Return weather data for every location as a list of dicts."""
    rows = []
    for idx, loc in enumerate(LOCATIONS, start=1):
        try:
            w = fetch_weather(loc["lat"], loc["lon"])
            condition = WEATHER_CODES.get(w["weathercode"], "Unknown")
            rows.append({
                "rank": idx,
                "country": loc["country"],
                "capital": loc["capital"],
                "temperature": _fallback(w["temperature"]),
                "windspeed": _fallback(w["windspeed"]),
                "humidity": _fallback(w["humidity"]),
                "rainfall": _fallback(w["rainfall"]),
                "condition": condition,
            })
        except Exception as exc:
            print(f"⚠️  Warning: failed to fetch weather for {loc['capital']}: {exc}")
            rows.append({
                "rank": idx,
                "country": loc["country"],
                "capital": loc["capital"],
                "temperature": "N/A",
                "windspeed": "N/A",
                "humidity": "N/A",
                "rainfall": "N/A",
                "condition": "N/A",
            })
    return rows


def main() -> None:
    print("🌍 Global Weather Report — Top 10 Countries + Indian Metro Cities")
    print()

    data = get_weather_data()
    table = [
        [r["rank"], r["country"], r["capital"], r["temperature"],
         r["windspeed"], r["humidity"], r["rainfall"], r["condition"]]
        for r in data
    ]
    print(tabulate(table, headers=TABLE_HEADERS, tablefmt="fancy_grid"))

    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f"\n📅 Data fetched at: {timestamp}")


if __name__ == "__main__":
    main()

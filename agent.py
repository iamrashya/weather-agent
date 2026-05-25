"""Weather Agent — fetches real-time weather for the top 10 most populous countries
using the free Open-Meteo API (no API key required) and displays a terminal table.
"""

from datetime import datetime

import requests
from tabulate import tabulate


# Top 10 most populous countries with their capital city coordinates.
COUNTRIES = [
    {"country": "China",      "capital": "Beijing",      "lat": 39.9042,  "lon": 116.4074},
    {"country": "India",      "capital": "New Delhi",    "lat": 28.6139,  "lon": 77.2090},
    {"country": "USA",        "capital": "Washington DC","lat": 38.9072,  "lon": -77.0369},
    {"country": "Indonesia",  "capital": "Jakarta",      "lat": -6.2088,  "lon": 106.8456},
    {"country": "Pakistan",   "capital": "Islamabad",    "lat": 33.6844,  "lon": 73.0479},
    {"country": "Brazil",     "capital": "Brasilia",     "lat": -15.7942, "lon": -47.8822},
    {"country": "Nigeria",    "capital": "Abuja",        "lat": 9.0765,   "lon": 7.3986},
    {"country": "Bangladesh", "capital": "Dhaka",        "lat": 23.8103,  "lon": 90.4125},
    {"country": "Russia",     "capital": "Moscow",       "lat": 55.7558,  "lon": 37.6173},
    {"country": "Ethiopia",   "capital": "Addis Ababa",  "lat": 9.0320,   "lon": 38.7469},
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


def fetch_weather(lat: float, lon: float) -> dict:
    """Call the Open-Meteo API and return the current_weather block."""
    response = requests.get(
        API_URL,
        params={"latitude": lat, "longitude": lon, "current_weather": "true"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json().get("current_weather", {})


def build_row(rank: int, entry: dict) -> list:
    """Return a table row for one country, falling back to N/A on failure."""
    try:
        current = fetch_weather(entry["lat"], entry["lon"])
        temperature = current.get("temperature", "N/A")
        windspeed = current.get("windspeed", "N/A")
        code = current.get("weathercode")
        condition = WEATHER_CODES.get(code, "Unknown")
    except Exception as exc:
        print(f"⚠️  Warning: failed to fetch weather for {entry['country']}: {exc}")
        temperature = windspeed = condition = "N/A"

    return [rank, entry["country"], entry["capital"], temperature, windspeed, condition]


def main() -> None:
    print("🌍 Global Weather Report — Top 10 Most Populous Countries")
    print()

    rows = [build_row(i + 1, entry) for i, entry in enumerate(COUNTRIES)]

    headers = ["Rank", "Country", "Capital", "Temperature (°C)", "Wind Speed (km/h)", "Condition"]
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f"\n📅 Data fetched at: {timestamp}")


if __name__ == "__main__":
    main()

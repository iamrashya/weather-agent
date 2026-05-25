"""Flask web dashboard for the Weather Agent."""

from datetime import datetime

from flask import Flask, render_template_string, send_file

from agent import get_weather_data
from export_pdf import generate_pdf


app = Flask(__name__)


CONDITION_EMOJI = {
    "Clear Sky": "☀️",
    "Mainly Clear": "☀️",
    "Partly Cloudy": "⛅",
    "Overcast": "☁️",
    "Foggy": "🌫️",
    "Icy Fog": "🌫️",
    "Light Drizzle": "🌦️",
    "Drizzle": "🌦️",
    "Heavy Drizzle": "🌦️",
    "Slight Rain": "🌧️",
    "Rain": "🌧️",
    "Heavy Rain": "🌧️",
    "Slight Snow": "❄️",
    "Snow": "❄️",
    "Heavy Snow": "❄️",
    "Rain Showers": "🌧️",
    "Heavy Rain Showers": "🌧️",
    "Thunderstorm": "⛈️",
    "Thunderstorm with Hail": "⛈️",
    "Unknown": "🌡️",
    "N/A": "🌡️",
}

TEMPLATE = """<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta http-equiv=\"refresh\" content=\"3600\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Global Weather Dashboard</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif;
      background: linear-gradient(135deg, #0b1d3a 0%, #000000 100%);
      color: #fff;
      padding: 40px 20px;
    }
    .container { max-width: 1200px; margin: 0 auto; }
    h1 { font-size: 2.5rem; margin: 0 0 8px; font-weight: 700; }
    .subtitle { color: #aaa; margin-bottom: 20px; }
    .card {
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 16px;
      padding: 20px;
      overflow-x: auto;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    table { width: 100%; border-collapse: collapse; color: #fff; }
    th, td { padding: 12px 14px; text-align: left; }
    thead th {
      background: rgba(11, 61, 145, 0.6);
      font-weight: 600;
      border-bottom: 1px solid rgba(255, 255, 255, 0.15);
      letter-spacing: 0.3px;
    }
    tbody tr:nth-child(odd) { background: rgba(255, 255, 255, 0.03); }
    tbody tr:nth-child(even) { background: rgba(255, 255, 255, 0.06); }
    tbody tr { transition: background 0.2s ease; }
    tbody tr:hover { background: rgba(80, 140, 220, 0.25); }
    .btn {
      display: inline-block;
      margin: 0 0 24px 0;
      padding: 12px 24px;
      background: #1f6feb;
      color: #fff;
      text-decoration: none;
      border-radius: 8px;
      font-weight: 600;
      box-shadow: 0 4px 14px rgba(31, 111, 235, 0.4);
    }
    .btn:hover { background: #3b82f6; }
    footer { color: #888; margin-top: 24px; font-size: 0.9rem; text-align: center; }
  </style>
</head>
<body>
  <div class=\"container\">
    <h1>🌍 Global Weather Dashboard</h1>
    <div class=\"subtitle\">Last updated: {{ timestamp }}</div>
    <a class=\"btn\" href=\"/download\">⬇️ Download PDF Report</a>
    <div class=\"card\">
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Country/City</th>
            <th>Capital/City</th>
            <th>Temp (°C)</th>
            <th>Wind (km/h)</th>
            <th>Humidity (%)</th>
            <th>Rainfall (mm)</th>
            <th>Condition</th>
          </tr>
        </thead>
        <tbody>
          {% for r in rows %}
          <tr>
            <td>{{ r.rank }}</td>
            <td>{{ r.country }}</td>
            <td>{{ r.capital }}</td>
            <td>{{ r.temperature }}</td>
            <td>{{ r.windspeed }}</td>
            <td>{{ r.humidity }}</td>
            <td>{{ r.rainfall }}</td>
            <td>{{ emoji.get(r.condition, '🌡️') }} {{ r.condition }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
    <footer>Data source: Open-Meteo &nbsp;|&nbsp; Auto-refreshes every 60 minutes</footer>
  </div>
</body>
</html>
"""


@app.route("/")
def index():
    rows = get_weather_data()
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return render_template_string(TEMPLATE, rows=rows, timestamp=timestamp, emoji=CONDITION_EMOJI)


@app.route("/download")
def download():
    data = get_weather_data()
    pdf_path = generate_pdf(data)
    return send_file(pdf_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

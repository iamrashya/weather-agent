# Weather Agent — CLAUDE.md

## Project Purpose
A Python agent that fetches real-time weather for the top 10 most populous 
countries in the world using the free Open-Meteo API and displays results 
as a formatted table in the terminal.

## Tech Stack
- Language: Python 3.10+
- HTTP requests: requests library
- Table display: tabulate library (fancy_grid format)
- Environment variables: python-dotenv
- API: Open-Meteo (https://open-meteo.com) — free, no API key needed

## Project Structure
- agent.py          → main agent logic, entry point
- requirements.txt  → all Python dependencies
- .env              → environment variables (not committed to GitHub)
- venv/             → Python virtual environment (not committed to GitHub)
- README.md         → project documentation for GitHub

## How to Run
1. python -m venv venv
2. venv\Scripts\activate  (Windows) or source venv/bin/activate (Mac/Linux)
3. pip install -r requirements.txt
4. python agent.py

## Key Notes for Claude Code
- This is a pure Python project — do not use Node.js or npm
- Virtual environment folder is "venv" — never modify it directly
- .env is in .gitignore — never push it to GitHub
- If adding new countries, follow the same dictionary structure in agent.py
- The weathercode mapping dictionary is inside agent.py — update it there
- Table format uses tabulate fancy_grid — do not change the format
- API endpoint pattern: https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true

## Future Improvements (ideas for later)
- Add humidity and rainfall data when available from Open-Meteo
- Export table to CSV or PDF
- Add a simple web UI using Flask
- Schedule the agent to run every hour automatically

## GitHub Repository
https://github.com/iamrashya/weather-agent

## New Features Added
- Humidity and rainfall data from Open-Meteo hourly API
- PDF export using reportlab → saved to /reports folder
- Flask web dashboard at http://localhost:5000
- Hourly scheduler using schedule library
- Email sender using Gmail SMTP with PDF attachment
- Indian metro cities added to the weather list

## New Files
- export_pdf.py   → generates PDF weather report
- send_email.py   → sends email with PDF attachment via Gmail
- app.py          → Flask web dashboard on port 5000
- scheduler.py    → runs full workflow every 60 minutes

## How to Run Each Feature
- Terminal table only:     python agent.py
- Web dashboard:           python app.py → open http://localhost:5000
- Full hourly scheduler:   python scheduler.py
- One-time PDF + email:    python scheduler.py (runs once immediately)

## Environment Variables Needed in .env
- GITHUB_USERNAME
- REPO_NAME
- GMAIL_SENDER
- GMAIL_RECIPIENTS
- GMAIL_APP_PASSWORD

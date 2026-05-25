"""Hourly scheduler — runs the full weather workflow every 60 minutes.

Workflow on each tick:
  1. Fetch weather data
  2. Print the table to the terminal
  3. Generate a PDF report into /reports
  4. Email the PDF to all GMAIL_RECIPIENTS
"""

import time
from datetime import datetime

import schedule
from tabulate import tabulate

from agent import TABLE_HEADERS, get_weather_data
from export_pdf import generate_pdf
from send_email import send_weather_email


def run_job() -> None:
    print(f"🔄 Running weather report job at: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    data = get_weather_data()

    table = [
        [r["rank"], r["country"], r["capital"], r["temperature"],
         r["windspeed"], r["humidity"], r["rainfall"], r["condition"]]
        for r in data
    ]
    print(tabulate(table, headers=TABLE_HEADERS, tablefmt="fancy_grid"))

    pdf_path = generate_pdf(data)
    print(f"📄 PDF saved: {pdf_path}")

    send_weather_email(pdf_path, data)

    print("✅ Job complete — next run in 60 minutes")


if __name__ == "__main__":
    print("🕐 Scheduler started — weather report will run every 60 minutes")
    run_job()
    schedule.every(60).minutes.do(run_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

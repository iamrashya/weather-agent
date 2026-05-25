"""Send the weather report via Gmail SMTP with the PDF attached."""

import os
import smtplib
import ssl
from datetime import datetime
from email.message import EmailMessage

from dotenv import load_dotenv


def send_weather_email(pdf_path: str, weather_data=None) -> bool:
    """Send pdf_path as an attachment to all GMAIL_RECIPIENTS. Returns True on success."""
    load_dotenv()
    sender = os.getenv("GMAIL_SENDER")
    recipients_raw = os.getenv("GMAIL_RECIPIENTS", "")
    # Gmail App Passwords are 16 chars shown as 4 groups of 4 — strip spaces just in case.
    password = (os.getenv("GMAIL_APP_PASSWORD") or "").replace(" ", "")
    recipients = [r.strip() for r in recipients_raw.split(",") if r.strip()]

    if not sender or not recipients or not password or password == "YOUR_APP_PASSWORD_HERE":
        print("❌ Email config missing or placeholder — set GMAIL_SENDER, GMAIL_RECIPIENTS, GMAIL_APP_PASSWORD in .env")
        return False

    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    timestamp = now.strftime("%d-%m-%Y %H:%M:%S")

    msg = EmailMessage()
    msg["Subject"] = f"🌍 Weather Report — {date_str}"
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg.set_content(
        "Hello,\n\n"
        "Please find attached the latest Global Weather Report.\n\n"
        "This report includes real-time weather data for the\n"
        "top 10 most populous countries and major Indian metro cities.\n\n"
        "Data Source: Open-Meteo (open-meteo.com)\n"
        f"Generated at: {timestamp}\n\n"
        "Regards,\n"
        "Weather Agent 🌍"
    )

    try:
        with open(pdf_path, "rb") as fh:
            msg.add_attachment(
                fh.read(),
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(pdf_path),
            )
    except OSError as exc:
        print(f"❌ Could not attach PDF at {pdf_path}: {exc}")
        return False

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        print("✅ Email sent successfully to all recipients")
        return True
    except smtplib.SMTPAuthenticationError as exc:
        print(f"❌ Gmail authentication failed — check GMAIL_APP_PASSWORD: {exc}")
    except Exception as exc:
        print(f"❌ Failed to send email: {exc}")
    return False

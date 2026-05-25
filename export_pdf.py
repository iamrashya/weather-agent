"""PDF export for the weather report using reportlab."""

import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")

PDF_HEADERS = [
    "Rank", "Country/City", "Capital/City", "Temp (°C)",
    "Wind (km/h)", "Humidity (%)", "Rainfall (mm)", "Condition",
]


def generate_pdf(weather_data, filename: str | None = None) -> str:
    """Render weather_data into a styled PDF and return the saved file path."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    if filename is None:
        stamp = datetime.now().strftime("%d%m%Y_%H%M%S")
        filename = os.path.join(REPORTS_DIR, f"weather_report_{stamp}.pdf")

    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(A4),
        title="Global Weather Report",
        leftMargin=24, rightMargin=24, topMargin=24, bottomMargin=24,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle", parent=styles["Title"],
        fontSize=16, alignment=1, spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle", parent=styles["Normal"],
        fontSize=10, alignment=1, textColor=colors.grey, spaceAfter=12,
    )

    story = [
        Paragraph("Global Weather Report", title_style),
        Paragraph(
            f"Generated at: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            subtitle_style,
        ),
        Spacer(1, 6),
    ]

    table_data = [PDF_HEADERS]
    for r in weather_data:
        table_data.append([
            r["rank"], r["country"], r["capital"], r["temperature"],
            r["windspeed"], r["humidity"], r["rainfall"], r["condition"],
        ])

    style_cmds = [
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#0B3D91")),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING",(0, 0), (-1, 0), 8),
        ("TOPPADDING",   (0, 0), (-1, 0), 8),
        ("GRID",         (0, 0), (-1, -1), 0.25, colors.grey),
    ]
    for i in range(1, len(table_data)):
        bg = colors.white if i % 2 == 1 else colors.HexColor("#E6F0FA")
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle(style_cmds))
    story.append(table)

    doc.build(story)
    return filename


if __name__ == "__main__":
    from agent import get_weather_data
    path = generate_pdf(get_weather_data())
    print(f"📄 PDF saved: {path}")

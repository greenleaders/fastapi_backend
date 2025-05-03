from fastapi import FastAPI, HTTPException, Response
import requests
import ollama
from fpdf import FPDF
from pydantic import BaseModel, Field
import os
from datetime import datetime
from typing import List

# Create FastAPI app instance
app = FastAPI(title="AI-Powered Precision Agriculture API", version="2.0")

# Constants
LOGO_PATH = "images/clear_logo.png"
COMPANY_NAME = "Green Leaders Network"
COMPANY_EMAIL = "greenleadersnetwork@gmail.com"
COMPANY_ADDRESS = "Kigali, Rwanda"
WEATHER_API_KEY = "b3df74439236150a3119e1f968ae1e71"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Models
class FieldPoint(BaseModel):
    soil_ph: float = Field(..., ge=0, le=14, description="Soil pH level (0-14)")
    nitrogen: float = Field(..., ge=0, description="Nitrogen level in mg/kg")
    phosphorus: float = Field(..., ge=0, description="Phosphorus level in mg/kg")
    potassium: float = Field(..., ge=0, description="Potassium level in mg/kg")
    soil_moisture: float = Field(..., ge=0, le=100, description="Soil moisture percentage (0-100%)")

class CropAdvisoryRequest(BaseModel):
    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country name")
    points: List[FieldPoint] = Field(..., min_items=1, description="List of field soil data points")
    crop_type: str = Field(..., description="Type of crop")
    growth_stage: str = Field(..., description="Crop growth stage (e.g., Seedling, Flowering, Harvesting)")

# AI-powered crop advisory function
def interpret_crop_data(data: FieldPoint, crop_type: str, growth_stage: str) -> str:
    """
    Uses Ollama AI to analyze soil data and provide crop recommendations.
    """
    try:
        prompt = f"""
        Analyze the following soil and crop data and provide expert recommendations:

        - Soil pH: {data.soil_ph}
        - Nitrogen: {data.nitrogen} mg/kg
        - Phosphorus: {data.phosphorus} mg/kg
        - Potassium: {data.potassium} mg/kg
        - Soil Moisture: {data.soil_moisture}%
        - Crop Type: {crop_type}
        - Growth Stage: {growth_stage}

        Please provide:
        1. Nutrient adjustment recommendations (specific values for N, P, K)
        2. Soil health improvement advice
        3. Expected crop performance given the current soil condition
        """

        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])

        if "message" in response and "content" in response["message"]:
            return response["message"]["content"]
        else:
            return "AI response error: Unable to generate advisory."
    
    except Exception as e:
        return f"Error processing AI response: {str(e)}"

# Function to generate a PDF report
def generate_pdf(title, content, point_reports=None, summary_report=None) -> bytes:
    """
    Creates a PDF document containing soil analysis and crop recommendations.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)

    # Add logo
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=10, y=10, w=40)
    pdf.ln(10)

    # Header
    pdf.set_text_color(0, 100, 0)
    pdf.cell(0, 10, COMPANY_NAME, ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Email: {COMPANY_EMAIL}", ln=True, align='C')
    pdf.cell(0, 10, f"Address: {COMPANY_ADDRESS}", ln=True, align='C')
    pdf.ln(10)

    # Title
    pdf.set_font("Arial", style='B', size=14)
    pdf.set_fill_color(0, 100, 0)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, title, ln=True, align='C', fill=True)
    pdf.ln(10)

    # Timestamp
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)

    # Main Content
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, content)
    pdf.ln(10)

    # Field Point Reports
    if point_reports:
        pdf.set_font("Arial", size=12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, "Field Point Analysis", ln=True, align='C', fill=True)
        for i, report in enumerate(point_reports, 1):
            pdf.ln(5)
            pdf.cell(0, 10, f"Point {i} Analysis", ln=True, align='L')
            pdf.multi_cell(0, 10, report)
            pdf.ln(5)

    # Summary Report
    if summary_report:
        pdf.set_font("Arial", size=12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, "Overall Summary", ln=True, align='C', fill=True)
        pdf.multi_cell(0, 10, summary_report)

    return pdf.output(dest='S').encode('latin1')

# API endpoint to generate crop advisory PDF
@app.post("/crop-advisory/pdf")
def crop_advisory_pdf(data: CropAdvisoryRequest):
    """
    Generates a PDF advisory report based on provided crop and soil data.
    """
    try:
        point_reports = []
        summary_reports = []

        # Process each field point
        for point in data.points:
            report = interpret_crop_data(point, data.crop_type, data.growth_stage)
            point_reports.append(report)
            summary_reports.append(f"Point {len(summary_reports) + 1}: {report.split('.')[0]}")  # Extracting main recommendation

        overall_summary = "\n".join(summary_reports)

        # Generate PDF
        pdf_content = generate_pdf(
            "Crop Advisory Report",
            "Detailed Analysis and Recommendations",
            point_reports,
            overall_summary
        )

        return Response(content=pdf_content, media_type="application/pdf",
                        headers={"Content-Disposition": "attachment; filename=Crop_Advisory_Report.pdf"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

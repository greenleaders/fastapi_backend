from fastapi import FastAPI, HTTPException, Response
import requests
import ollama
from fpdf import FPDF
from pydantic import BaseModel
import os
from datetime import datetime
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://fastapi-backend-3-kguq.onrender.com/",  # Allow requests from your Django app's origin
    # Add other origins if needed (e.g., for production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (POST, GET, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# ... your other FastAPI routes ...

# Create FastAPI app instance
app = FastAPI(title="Artificial Intelligence Precision Agriculture LLM API", version="1.4")

# Constants and other configurations
LOGO_PATH = "images/clear_logo.png"
COMPANY_NAME = "Precision AI"
COMPANY_EMAIL = "precisionai@gmail.com"
COMPANY_ADDRESS = "Kigali, Rwanda"
WEATHER_API_KEY = "b3df74439236150a3119e1f968ae1e71"
IP_GEOLOCATION_API = "https://ipinfo.io/json"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_API_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Models
class FieldPoint(BaseModel):
    soil_ph: float
    nitrogen: float
    phosphorus: float
    potassium: float
    soil_moisture: float

class CropAdvisoryRequest(BaseModel):
    city: str = None
    country: str = None
    points: List[FieldPoint]
    crop_type: str
    growth_stage: str

# Function to interpret data for each point using AI (Ollama model)
def interpret_crop_data(data: FieldPoint, crop_type: str, growth_stage: str):
    prompt = f"""
    Given the following soil and crop data:
    - Soil pH: {data.soil_ph} pH
    - Nitrogen: {data.nitrogen} mg/kg
    - Phosphorus: {data.phosphorus} mg/kg
    - Potassium: {data.potassium} mg/kg
    - Soil Moisture: {data.soil_moisture}%
    - Crop Type: {crop_type}
    - Growth Stage: {growth_stage}
    
    Provide the following advisory:
    1. Nutrient recommendation: How much Nitrogen, Phosphorus, and Potassium should be added based on the soil values?
    2. Additional recommendations for soil improvement, including any other necessary treatments.
    3. An overall assessment of how the crop will perform given the current soil conditions.
    """
    
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Function to generate the advisory PDF report
def generate_pdf(title, content, point_reports=None, summary_report=None):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)

    # Add logo if it exists
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=10, y=10, w=40)
    pdf.ln(10)

    # Add header
    pdf.set_text_color(0, 100, 0)
    pdf.cell(0, 10, COMPANY_NAME, ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Email: {COMPANY_EMAIL}", ln=True, align='C')
    pdf.cell(0, 10, f"Address: {COMPANY_ADDRESS}", ln=True, align='C')
    pdf.ln(10)

    # Title section
    pdf.set_font("Arial", style='B', size=14)
    pdf.set_fill_color(0, 100, 0)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, title, ln=True, align='C', fill=True)
    pdf.ln(10)

    # Timestamp
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)

    # Main content (general report)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, content)
    pdf.ln(10)

    # Point-wise analysis (if available)
    if point_reports:
        pdf.set_font("Arial", size=12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, "Field Point Analysis Reports", ln=True, align='C', fill=True)
        for i, report in enumerate(point_reports, 1):
            pdf.ln(5)
            pdf.cell(0, 10, f"Point {i} Analysis", ln=True, align='L')
            pdf.multi_cell(0, 10, report)
            pdf.ln(5)

    # Summary report (including nutrient recommendations)
    if summary_report:
        pdf.set_font("Arial", size=12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, "Overall Summary Report", ln=True, align='C', fill=True)
        pdf.multi_cell(0, 10, summary_report)

    return pdf.output(dest='S').encode('latin1')

# API endpoint to handle crop advisory report creation
@app.post("/crop-advisory/pdf")
def crop_advisory_pdf(data: CropAdvisoryRequest):
    
    if not data.city or not data.country:
        raise HTTPException(status_code=400, detail="City and Country are required.")

    point_reports = []
    summary_reports = []
    
    # Collect individual reports and generate recommendations for each point
    for point in data.points:
        report = interpret_crop_data(point, data.crop_type, data.growth_stage)
        point_reports.append(report)
        
        # Extract nutrient recommendations from the report
        # For simplicity, let's assume the recommendations are within the report text
        # You can adjust this to better extract the data from the response
        nutrient_recommendations = "Add X amount of Nitrogen, Y amount of Phosphorus, Z amount of Potassium."
        #summary_reports.append(f"Point {len(summary_reports) + 1}: {nutrient_recommendations}")
    
    # Combine individual reports into one overall report
    overall_summary = "\n".join(summary_reports)

    # Generate final PDF
    pdf_content = generate_pdf("Crop Advisory Report", "Individual Analysis for Each Field Point:", point_reports, overall_summary)

    return Response(content=pdf_content, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=Crop_Advisory_Report.pdf"})
 
 

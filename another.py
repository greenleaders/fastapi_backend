from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fpdf import FPDF
from fastapi.responses import Response
from typing import List

# Create FastAPI app instance
app = FastAPI(title="Crop Advisory PDF Generator", version="1.0")

# Define the Pydantic models for the request payload
class FieldPoint(BaseModel):
    soil_ph: float
    nitrogen: float
    phosphorus: float
    potassium: float
    soil_moisture: float

class CropAdvisoryRequest(BaseModel):
    city: str
    country: str
    crop_type: str
    growth_stage: str
    points: List[FieldPoint]

# Function to generate the advisory PDF report
def generate_pdf(title: str, content: str, points_data: List[FieldPoint]):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)

    # Title section
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)

    # Content section (general report)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.ln(10)

    # Point-wise analysis
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Field Point Analysis", ln=True, align='C')
    pdf.ln(5)
    
    for i, point in enumerate(points_data, 1):
        pdf.cell(0, 10, f"Point {i} Analysis", ln=True, align='L')
        point_details = f"  Soil pH: {point.soil_ph}, Nitrogen: {point.nitrogen} mg/kg, Phosphorus: {point.phosphorus} mg/kg, Potassium: {point.potassium} mg/kg, Soil Moisture: {point.soil_moisture}%"
        pdf.multi_cell(0, 10, point_details)
        pdf.ln(5)

    return pdf.output(dest='S').encode('latin1')

# API endpoint to accept the payload and return a PDF
@app.post("/crop-advisory/pdf")
async def crop_advisory_pdf(data: CropAdvisoryRequest):
    # Generate the advisory report content
    content = f"City: {data.city}\nCountry: {data.country}\nCrop Type: {data.crop_type}\nGrowth Stage: {data.growth_stage}\n\n"
    content += "Soil and Crop Analysis for Each Field Point:\n"

    # Generate PDF from the data
    pdf_content = generate_pdf(
        title=f"Crop Advisory Report for {data.crop_type} in {data.city}, {data.country}",
        content=content,
        points_data=data.points
    )

    return Response(content=pdf_content, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=Crop_Advisory_Report.pdf"})


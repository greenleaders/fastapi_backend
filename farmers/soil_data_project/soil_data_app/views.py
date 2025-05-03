import requests
from django.shortcuts import render
from django.http import HttpResponse
from .forms import SoilDataForm

FASTAPI_URL = "https://fastapi-backend-2-jups.onrender.com/crop-advisory/pdf"  # Update with the actual API URL

def home_view(request):
    return render(request, "home.html")

def submit_data(request):
    if request.method == "POST":
        form = SoilDataForm(request.POST)
        if form.is_valid():
            data = {
                "city": form.cleaned_data["city"],
                "country": form.cleaned_data["country"],
                "crop_type": form.cleaned_data["crop_type"],
                "growth_stage": form.cleaned_data["growth_stage"],
                "points": []
            }

            for i in range(len(request.POST.getlist("soil_ph"))):
                point = {
                    "soil_ph": float(request.POST.getlist("soil_ph")[i]),
                    "nitrogen": float(request.POST.getlist("nitrogen")[i]),
                    "phosphorus": float(request.POST.getlist("phosphorus")[i]),
                    "potassium": float(request.POST.getlist("potassium")[i]),
                    "soil_moisture": float(request.POST.getlist("soil_moisture")[i])
                }
                data["points"].append(point)

            # Send data to FastAPI to generate the PDF
            response = requests.post(FASTAPI_URL, json=data)

            if response.status_code == 200:
                pdf_content = response.content
                response = HttpResponse(pdf_content, content_type="application/pdf")
                response["Content-Disposition"] = 'inline; filename="Crop_Advisory_Report.pdf"'
                return response
            else:
                return HttpResponse("Error generating PDF report.", status=500)
    
    else:
        form = SoilDataForm()
    
    return render(request, "form.html", {"form": form})

import requests
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import CropDataForm

FASTAPI_URL = "http://127.0.0.1:8000/crop-advisory/pdf"  # Update if FastAPI is on a different port

def crop_advisory_view(request):
    if request.method == "POST":
        form = CropDataForm(request.POST)
        if form.is_valid():
            crop_type = form.cleaned_data['crop_type']
            growth_stage = form.cleaned_data['growth_stage']
            city = form.cleaned_data['city']
            country = form.cleaned_data['country']
            
            field_points = []
            index = 1
            while f'point-{index}-soil_ph' in request.POST:
                try:
                    field_points.append({
                        "soil_ph": float(request.POST[f'point-{index}-soil_ph']),
                        "nitrogen": float(request.POST[f'point-{index}-nitrogen']),
                        "phosphorus": float(request.POST[f'point-{index}-phosphorus']),
                        "potassium": float(request.POST[f'point-{index}-potassium']),
                        "soil_moisture": float(request.POST[f'point-{index}-soil_moisture']),
                    })
                except ValueError:
                    return JsonResponse({"error": f"Invalid data at point-{index}"}, status=400)
                index += 1

            payload = {
                "city": city,
                "country": country,
                "crop_type": crop_type,
                "growth_stage": growth_stage,
                "points": field_points
            }

            print("\n\n===== DEBUG: Sending Request to FastAPI =====")
            print("URL:", FASTAPI_URL)
            print("Payload:", json.dumps(payload, indent=4))
            
            try:
                response = requests.post(
                    FASTAPI_URL, json=payload, headers={"Content-Type": "application/json"}
                )
                print("FastAPI Response Code:", response.status_code)
                print("FastAPI Response Body:", response.text)

                if response.status_code == 200:
                    pdf_filename = "Crop_Advisory_Report.pdf"
                    return HttpResponse(
                        response.content,
                        content_type="application/pdf",
                        headers={"Content-Disposition": f"inline; filename={pdf_filename}"}
                    )
                else:
                    return JsonResponse({
                        "error": f"API request failed: {response.status_code}, {response.text}"
                    }, status=response.status_code)

            except requests.exceptions.RequestException as e:
                return JsonResponse({"error": f"Failed to connect to FastAPI: {str(e)}"}, status=500)
    
    else:
        form = CropDataForm()

    return render(request, "crop_advisory/form.html", {"form": form})

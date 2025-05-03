# advisory/views.py
from django.shortcuts import render
from django.http import JsonResponse
import requests

def crop_advisory_form(request):
    if request.method == 'POST':
        # Extract form data
        city = request.POST.get('city')
        country = request.POST.get('country')
        crop_type = request.POST.get('crop_type')
        growth_stage = request.POST.get('growth_stage')

        # Collect all the points data
        points = []
        point_count = len([key for key in request.POST.keys() if key.startswith('soil_ph')])

        for i in range(1, point_count + 1):
            point = {
                'soil_ph': float(request.POST.get(f"soil_ph{i}")),
                'nitrogen': float(request.POST.get(f"nitrogen{i}")),
                'phosphorus': float(request.POST.get(f"phosphorus{i}")),
                'potassium': float(request.POST.get(f"potassium{i}")),
                'soil_moisture': float(request.POST.get(f"soil_moisture{i}"))
            }
            points.append(point)

        # Prepare data to send to FastAPI
        advisory_data = {
            'city': city,
            'country': country,
            'crop_type': crop_type,
            'growth_stage': growth_stage,
            'points': points
        }

        # Send data to FastAPI endpoint (update URL as needed)
        fastapi_url = "http://127.0.0.1:8000/crop-advisory/pdf"
        response = requests.post(fastapi_url, json=advisory_data)

        if response.status_code == 200:
            # Return the PDF to the user
            return JsonResponse({'message': 'PDF Generated', 'pdf_content': response.content})
        else:
            return JsonResponse({'message': 'Error generating PDF'}, status=500)

    return render(request, 'crop_advisory_form.html')
# advisory/views.py
from django.shortcuts import render

 

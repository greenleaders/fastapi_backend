import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# FastAPI URL for crop advisory PDF generation
FASTAPI_URL = "http://127.0.0.1:8000/crop-advisory/pdf"  # Update with your FastAPI endpoint

# View to render the template and handle the form submission
@csrf_exempt  # Disable CSRF validation for this view, or use Django CSRF token appropriately
def generate_advisory_pdf(request):
    if request.method == 'POST':
        # Retrieve crop data from the form
        crop_type = request.POST.get('crop_type')
        growth_stage = request.POST.get('growth_stage')
        points = []

        # Extract data for each field point dynamically
        for key in request.POST:
            if key.startswith('point-'):
                point_index = key.split('-')[1]
                soil_ph = request.POST.get(f'point-{point_index}-soil_ph')
                nitrogen = request.POST.get(f'point-{point_index}-nitrogen')
                phosphorus = request.POST.get(f'point-{point_index}-phosphorus')
                potassium = request.POST.get(f'point-{point_index}-potassium')
                soil_moisture = request.POST.get(f'point-{point_index}-soil_moisture')

                points.append({
                    'soil_ph': soil_ph,
                    'nitrogen': nitrogen,
                    'phosphorus': phosphorus,
                    'potassium': potassium,
                    'soil_moisture': soil_moisture
                })

        # Prepare data to send to FastAPI
        data = {
            'crop_type': crop_type,
            'growth_stage': growth_stage,
            'points': points,
        }

        # Send the data to FastAPI via POST request
        headers = {'Content-Type': 'application/json'}
        response = requests.post(FASTAPI_URL, json=data, headers=headers)

        if response.status_code == 200:
            # FastAPI returns the PDF in base64 encoding
            pdf_base64 = response.json().get('pdf_base64')

            # Return the PDF base64 data in the response
            return JsonResponse({'pdf_base64': pdf_base64})

        # If FastAPI response is not OK, return an error
        return JsonResponse({'error': 'Error generating the PDF'}, status=400)

    # For GET request, render the advisory_home.html template
    return render(request, 'advisory/advisory_home.html')
# views.py

def advisory_home(request):
    return render(request, 'advisory_home.html')

import json
import requests
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Endpoint for the FastAPI to generate the report
FASTAPI_URL = "http://127.0.0.1:8000/crop-advisory/pdf"  # Update this URL if needed

# Geolocation API endpoint
GEOLOCATION_API = "https://ipinfo.io/json"

def crop_data_analysis(request):
    return render(request, 'advisory/crop_data_analysis.html')

@csrf_exempt
def generate_advisory_pdf(request):
    if request.method == 'POST':
        try:
            # Initialize empty JSON data
            data = {
                "city": "",
                "country": "",
                "points": [],
                "crop_type": "",
                "growth_stage": ""
            }

            # Detect user's location (city & country)
            geo_response = requests.get(GEOLOCATION_API)
            if geo_response.status_code == 200:
                location_data = geo_response.json()
                data["city"] = location_data.get("city", "Unknown City")
                data["country"] = location_data.get("country", "Unknown Country")

            # Determine if request is JSON or form-data
            if request.content_type == "application/json":
                request_data = json.loads(request.body)
                data["crop_type"] = request_data.get("crop_type", "")
                data["growth_stage"] = request_data.get("growth_stage", "")
                data["points"] = request_data.get("points", [])
            else:
                # Extract form-data
                data["crop_type"] = request.POST.get("crop_type", "")
                data["growth_stage"] = request.POST.get("growth_stage", "")

                i = 1
                while request.POST.get(f'point-{i}-soil_ph'):
                    try:
                        point = {
                            "soil_ph": float(request.POST.get(f'point-{i}-soil_ph', 0)),
                            "nitrogen": float(request.POST.get(f'point-{i}-nitrogen', 0)),
                            "phosphorus": float(request.POST.get(f'point-{i}-phosphorus', 0)),
                            "potassium": float(request.POST.get(f'point-{i}-potassium', 0)),
                            "soil_moisture": float(request.POST.get(f'point-{i}-soil_moisture', 0))
                        }
                        data["points"].append(point)
                    except ValueError:
                        logging.warning(f"Invalid data at point-{i}, skipping entry.")
                    i += 1

            # Log request payload
            logging.info(f"Sending data to FastAPI: {json.dumps(data, indent=2)}")

            # Validate required fields
            if not data["crop_type"] or not data["growth_stage"] or not data["points"]:
                logging.error("Missing required fields in the request.")
                return JsonResponse({"error": "Missing required fields: crop_type, growth_stage, or points"}, status=400)

            # Send data to FastAPI
            response = requests.post(FASTAPI_URL, json=data, headers={"Content-Type": "application/json"})

            if response.status_code == 200:
                # If response is OK, return the PDF content
                pdf_content = response.content
                return HttpResponse(pdf_content, content_type='application/pdf')
            else:
                logging.error(f"Error from FastAPI: {response.text}")
                return JsonResponse({"error": "Failed to generate advisory PDF."}, status=response.status_code)

        except json.JSONDecodeError:
            logging.error("Invalid JSON format received.")
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        except requests.RequestException as e:
            logging.error(f"Request error: {str(e)}")
            return JsonResponse({"error": "Error connecting to FastAPI service."}, status=500)

        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

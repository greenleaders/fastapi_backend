from django.shortcuts import render
import requests
from .forms import CropAdvisoryForm

API_URL = "http://127.0.0.1:8000/crop-advisory/pdf"

def advisory_view(request):
    pdf_url = None
    if request.method == "POST":
        form = CropAdvisoryForm(request.POST)
        if form.is_valid():
            data = {
                "city": form.cleaned_data["city"],
                "country": form.cleaned_data["country"],
                "crop_type": form.cleaned_data["crop_type"],
                "growth_stage": form.cleaned_data["growth_stage"],
                "points": eval(form.cleaned_data["points"]),
            }
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                pdf_url = response.url

    else:
        form = CropAdvisoryForm()

    return render(request, "advisory/form.html", {"form": form, "pdf_url": pdf_url})

# advisory/forms.py
from django import forms

class CropAdvisoryForm(forms.Form):
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    crop_type = forms.CharField(max_length=100)
    growth_stage = forms.CharField(max_length=100)
    soil_ph = forms.FloatField()
    nitrogen = forms.FloatField()
    phosphorus = forms.FloatField()
    potassium = forms.FloatField()
    soil_moisture = forms.FloatField()

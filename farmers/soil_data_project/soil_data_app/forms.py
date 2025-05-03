from django import forms

class SoilDataForm(forms.Form):
    city = forms.CharField(label="City")
    country = forms.CharField(label="Country")
    crop_type = forms.CharField(label="Crop Type")
    growth_stage = forms.CharField(label="Growth Stage")

    # Fields for multiple soil points
    soil_ph = forms.FloatField(label="Soil pH")
    nitrogen = forms.IntegerField(label="Nitrogen")
    phosphorus = forms.IntegerField(label="Phosphorus")
    potassium = forms.IntegerField(label="Potassium")
    soil_moisture = forms.IntegerField(label="Soil Moisture")

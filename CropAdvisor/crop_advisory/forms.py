from django import forms

class CropDataForm(forms.Form):
    crop_type = forms.CharField(label="Crop Type", max_length=100, required=True)
    growth_stage = forms.CharField(label="Growth Stage", max_length=100, required=True)
    city = forms.CharField(label="City", max_length=100, required=True)
    country = forms.CharField(label="Country", max_length=100, required=True)
    
    # Dynamic fields for soil data will be handled in the view.

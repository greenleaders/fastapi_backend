from django import forms

class CropAdvisoryForm(forms.Form):
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    crop_type = forms.CharField(max_length=100)
    growth_stage = forms.CharField(max_length=100)
    points = forms.CharField(widget=forms.Textarea, help_text="Enter multiple points as JSON format")

import json
from django import forms

# Define the FieldPoint class to store field data
class FieldPoint:
    def __init__(self, soil_ph, nitrogen, phosphorus, potassium, soil_moisture):
        self.soil_ph = soil_ph
        self.nitrogen = nitrogen
        self.phosphorus = phosphorus
        self.potassium = potassium
        self.soil_moisture = soil_moisture

# Define the form for crop advisory input
class CropAdvisoryForm(forms.Form):
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    crop_type = forms.CharField(max_length=100)
    growth_stage = forms.CharField(max_length=100)

    # Allow user to input JSON data for multiple field points
    points = forms.CharField(widget=forms.Textarea, help_text="Enter soil data in JSON format")

    def clean_points(self):
        points_data = self.cleaned_data['points']
        try:
            # Attempt to parse the JSON data entered by the user
            points_list = json.loads(points_data)
            field_points = []

            # Iterate through each point and convert it into a FieldPoint object
            for point_data in points_list:
                # Make sure the necessary keys are in the point data
                if all(key in point_data for key in ['soil_ph', 'nitrogen', 'phosphorus', 'potassium', 'soil_moisture']):
                    field_points.append(FieldPoint(**point_data))
                else:
                    raise forms.ValidationError("Each field point must contain 'soil_ph', 'nitrogen', 'phosphorus', 'potassium', and 'soil_moisture' keys.")
            return field_points
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON format for field points")
        except Exception as e:
            # Catch any other unexpected errors
            raise forms.ValidationError(f"Error processing the points: {str(e)}")

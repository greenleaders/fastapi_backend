from django.db import models

class FieldPoint(models.Model):
    soil_ph = models.FloatField()
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    soil_moisture = models.FloatField()

class CropData(models.Model):
    crop_type = models.CharField(max_length=100)
    growth_stage = models.CharField(max_length=100)
    points = models.ManyToManyField(FieldPoint)  # Link multiple points to one crop data


from django.urls import path
from . import views

urlpatterns = [
    path('', views.crop_data_analysis, name='crop_data_analysis'),
    path('generate-advisory-pdf/', views.generate_advisory_pdf, name='generate_advisory_pdf')
]

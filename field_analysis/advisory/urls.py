from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_advisory_pdf, name='generate_advisory_pdf'),  # Set the appropriate URL name
]

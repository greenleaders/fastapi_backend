 

from django.urls import path
from .views import submit_data, home_view

urlpatterns = [
    path("", home_view, name="home"),  # Add this line for the root URL
    path("submit/", submit_data, name="submit_data"),
]

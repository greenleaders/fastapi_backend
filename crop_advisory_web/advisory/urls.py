from django.urls import path
from .views import advisory_view

urlpatterns = [
    path("", advisory_view, name="advisory"),
]

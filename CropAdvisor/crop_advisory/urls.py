from django.urls import path
from .views import crop_advisory_view

urlpatterns = [
    path('', crop_advisory_view, name='crop_advisory'),
]


# crop_advisory/urls.py
from django.contrib import admin
from django.urls import path
from advisory import views  # Import your views module here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.crop_advisory_form, name='home'),  # Root URL will render the crop advisory form
    path('crop-advisory/', views.crop_advisory_form, name='crop_advisory_form'),  # Another route for the advisory form
]

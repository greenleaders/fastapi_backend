from django.contrib import admin
from django.urls import path
from advisory import views  # Make sure this import is present

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.crop_advisory_form, name='home'),
    path('crop-advisory/', views.crop_advisory_form, name='crop_advisory_form'),
]

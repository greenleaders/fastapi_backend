from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# Home page view
def home_view(request):
    return render(request, 'home.html')  # This will render home.html

urlpatterns = [
    path('', home_view, name='home'),  # Empty path now serves home.html
    path('admin/', admin.site.urls),
    path('advisory/', include('advisory.urls')),  # Ensure advisory has its own urls.py
]


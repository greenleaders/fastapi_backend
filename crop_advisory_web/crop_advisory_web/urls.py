from django.contrib import admin
from django.urls import path, include  # ✅ Add include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Crop Advisory System!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('advisory/', include('advisory.urls')),  # Ensure 'advisory' app is included
    path('', home, name='home'),  # Add a root URL pattern
]

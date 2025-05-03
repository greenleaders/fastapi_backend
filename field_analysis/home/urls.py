from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('home.urls')),  # Root URL now points to home app
    path('admin/', admin.site.urls),
    path('advisory/', include('advisory.urls')),
]

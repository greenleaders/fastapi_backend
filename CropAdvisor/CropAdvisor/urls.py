 
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from crop_advisory.views import crop_advisory_view

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('crop-advisory/', crop_advisory_view, name='crop-advisory'),  # Crop advisory API
    path('', include('crop_advisory.urls')),
]

# Serve static and media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

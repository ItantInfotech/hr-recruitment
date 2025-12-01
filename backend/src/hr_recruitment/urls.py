"""
URL configuration for hr_recruitment project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # django-simple-captcha URLs
    path("captcha/", include("captcha.urls")),

    # Your recruitment app URLs
    path("", include("recruitment.urls")),

    path('', include('profiles.urls', namespace='profiles')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

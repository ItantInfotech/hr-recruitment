from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.home, name='home'),

    # Application Form Routes
    path("apply/", views.job_apply, name="job_apply"),
    path("success/", views.success_page, name="success"),
]

from django.urls import path
from . import views

urlpatterns = [
    # Home page at "/"
    path("", views.home, name="home"),

    # Candidate auth
    path("login/", views.candidate_login, name="candidate_login"),
    path("dashboard/", views.candidate_dashboard, name="candidate_dashboard"),

    path("register/", views.register, name="register"),
    path("register/success/", views.register_success, name="register_success"),
    # plus your vacancies URLs if added
]

from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Registration
from .forms import RegistrationForm, CandidateLoginForm


def register(request):
    DUMMY_OTP = "1234"

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get("otp")

            # Dummy OTP check
            if otp != DUMMY_OTP:
                form.add_error("otp", "Invalid OTP. Use 1234 for now.")
            else:
                Registration.objects.create(
                    full_name=form.cleaned_data["full_name"],
                    email=form.cleaned_data["email"],
                    phone=form.cleaned_data["phone"],
                    is_email_verified=True,
                    is_phone_verified=True,
                )
                messages.success(request, "Registration successful! Thank you.")
                return redirect("register_success")
    else:
        form = RegistrationForm()

    return render(request, "recruitment/register.html", {"form": form})

def register_success(request):
    return render(request, "recruitment/register_success.html")

def home(request):
    """
    Public landing page for the NCC Veteran Recruitment Portal.
    """
    return render(request, "recruitment/home.html")

def candidate_login(request):
    """
    Candidate login using Email + Phone + OTP (dummy OTP=1234 for now).
    """
    if request.method == "POST":
        form = CandidateLoginForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data["otp"]

            if otp != "1234":
                form.add_error("otp", "Invalid OTP. For demo use 1234.")
            else:
                # Mark the candidate as "logged in" in session (demo logic)
                request.session["candidate_logged_in"] = True
                request.session["candidate_email"] = form.cleaned_data["email"]
                request.session["candidate_phone"] = form.cleaned_data["phone"]
                return redirect("candidate_dashboard")
    else:
        form = CandidateLoginForm()

    return render(request, "recruitment/login.html", {"form": form})


def candidate_dashboard(request):
    """
    Simple placeholder dashboard after candidate login.
    Later we’ll connect this to Veteran profiles.
    """
    if not request.session.get("candidate_logged_in"):
        return redirect("candidate_login")

    context = {
        "candidate_email": request.session.get("candidate_email"),
        "candidate_phone": request.session.get("candidate_phone"),
    }
    return render(request, "recruitment/dashboard.html", context)




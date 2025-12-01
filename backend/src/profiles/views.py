from django.shortcuts import render, redirect
from django.contrib import messages
from .models import JobApplication


def home(request):
    return render(request, "profiles/home.html")


def job_apply(request):
    if request.method == "POST":
        data = request.POST
        files = request.FILES

        JobApplication.objects.create(
            # Personal Details
            salutation=data.get("salutation"),
            first_name=data.get("first_name"),
            middle_name=data.get("middle_name"),
            last_name=data.get("last_name"),
            father_husband_name=data.get("father_husband_name"),
            date_of_birth=data.get("date_of_birth"),
            gender=data.get("gender"),
            religion=data.get("religion"),
            marital_status=data.get("marital_status"),
            blood_group=data.get("blood_group"),
            nationality=data.get("nationality"),
            aadhaar_or_other=data.get("aadhaar_or_other"),

            # Contact
            phone=data.get("phone"),
            mobile=data.get("mobile"),
            email=data.get("email"),

            # Address
            address=data.get("address"),
            permanent_address=data.get("permanent_address"),
            country=data.get("country"),
            state=data.get("state"),
            city=data.get("city"),
            pin=data.get("pin"),

            # Education Summary
            degree=data.get("degree"),
            university=data.get("university"),
            edu_from=data.get("edu_from"),
            edu_to=data.get("edu_to"),
            percentage=data.get("percentage"),

            education_certificate=files.get("education_certificate"),

            # Experience
            exp_from=data.get("exp_from"),
            exp_to=data.get("exp_to"),
            organization=data.get("organization"),
            designation=data.get("designation"),
            responsibilities=data.get("responsibilities"),
            exp_proof=files.get("exp_proof"),

            # Salary & Experience Info
            current_salary=data.get("current_salary"),
            relevant_years_of_experience=data.get("relevant_years_of_experience"),
            notice_period=data.get("notice_period"),

            # Upload Documents
            photo=files.get("photo"),
            age_proof=files.get("age_proof"),
            address_proof=files.get("address_proof"),
            last_salary_proof=files.get("last_salary_proof"),
        )

        messages.success(request, "Your application has been submitted successfully!")
        return redirect("profiles:success")

    return render(request, "profiles/apply_form.html")


def success_page(request):
    return render(request, "profiles/success.html")

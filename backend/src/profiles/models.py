from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# -----------------------------
# CHOICES
# -----------------------------

ID_DOC_CHOICES = [
    ('aadhaar', 'Aadhaar Card'),
    ('voter', 'Voter Card'),
    ('driving', 'Driving License'),
    ('passport', 'Passport'),
    ('pan', 'PAN Card'),
]

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

MARITAL_CHOICES = [
    ('single', 'Single'),
    ('married', 'Married'),
    ('other', 'Other'),
]

BLOOD_GROUPS = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-'),
]

# -----------------------------
# MAIN MODELS
# -----------------------------

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    salutation = models.CharField(max_length=20, blank=True)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150)
    father_or_husband_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    religion = models.CharField(max_length=100, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_CHOICES, blank=True)

    address_permanent = models.TextField(blank=True)
    address_current = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    pin = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    id_doc_type = models.CharField(max_length=20, choices=ID_DOC_CHOICES, blank=True)
    id_doc_number = models.CharField(max_length=100, blank=True)

    computer_proficiency = models.JSONField(default=list, blank=True)
    languages_known = models.JSONField(default=list, blank=True)

    current_or_last_monthly_fee = models.CharField(max_length=100, blank=True)
    relevant_years_of_experience = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    notice_period = models.CharField(max_length=100, blank=True)

    photo = models.ImageField(upload_to='candidates/photos/', null=True, blank=True)
    age_proof = models.FileField(upload_to='candidates/proofs/age/', null=True, blank=True)
    address_proof = models.FileField(upload_to='candidates/proofs/address/', null=True, blank=True)
    last_salary_proof = models.FileField(upload_to='candidates/proofs/salary/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        parts = [self.salutation, self.first_name, self.middle_name, self.last_name]
        return " ".join([p for p in parts if p])

    def __str__(self):
        return f"{self.full_name()} ({self.email or self.mobile})"


class Education(models.Model):
    candidate = models.ForeignKey(CandidateProfile, related_name='educations', on_delete=models.CASCADE)
    degree = models.CharField(max_length=255)
    university = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    percentage = models.CharField(max_length=20, blank=True)
    certificate = models.FileField(upload_to='candidates/education_certificates/', null=True, blank=True)

    def __str__(self):
        return f"{self.degree} - {self.university}"


class Experience(models.Model):
    candidate = models.ForeignKey(CandidateProfile, related_name='experiences', on_delete=models.CASCADE)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    organization = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    responsibilities = models.TextField(blank=True)
    experience_proof = models.FileField(upload_to='candidates/experience_proofs/', null=True, blank=True)

    def __str__(self):
        return f"{self.designation} @ {self.organization}"


class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company}"


class JobApplication(models.Model):
    job = models.ForeignKey(Job, related_name='applications', on_delete=models.CASCADE)
    candidate = models.ForeignKey(CandidateProfile, related_name='job_applications', on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Applied')
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.candidate} -> {self.job} ({self.status})"

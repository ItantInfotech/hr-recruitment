from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ServiceBranch(models.Model):
    """
    Tri-service classification: Army, Navy, Air Force.
    """
    name = models.CharField(max_length=50, unique=True)  # e.g. Army, Navy, Air Force
    short_name = models.CharField(max_length=10, unique=True)  # e.g. ARMY, NAVY, AF

    def __str__(self):
        return self.name


class Rank(models.Model):
    """
    Rank as per service branch (JCO, NCO, Offr, etc.).
    """
    branch = models.ForeignKey(ServiceBranch, on_delete=models.CASCADE, related_name="ranks")
    name = models.CharField(max_length=100)          # e.g. Subedar Major
    abbreviation = models.CharField(max_length=20)   # e.g. Sub Maj
    order = models.PositiveIntegerField(default=0)   # for sorting (higher rank, lower number or vice versa)

    class Meta:
        unique_together = ("branch", "name")
        ordering = ["branch", "order", "name"]

    def __str__(self):
        return f"{self.abbreviation} ({self.branch.short_name})"


class Organization(models.Model):
    """
    Represents NCC Units, Group HQs, Directorates, HQ DG NCC.
    Hierarchical but keep it simple first.
    """
    TYPE_CHOICES = [
        ("UNIT", "NCC Unit"),
        ("GROUP", "Group HQ"),
        ("DIRECTORATE", "Directorate"),
        ("HQ_DGNCC", "HQ DG NCC"),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        help_text="Parent HQ (e.g., Unit → Group HQ → Directorate → HQ DGNCC).",
    )

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Veteran(models.Model):
    """
    Master veteran profile / database.
    """
    SERVICE_STATUS_CHOICES = [
        ("PENDING_VERIFICATION", "Pending Verification"),
        ("VERIFIED", "Verified"),
        ("REJECTED", "Rejected"),
    ]

    service_number = models.CharField(max_length=50, unique=True, help_text="Service number / ADN equivalent")
    branch = models.ForeignKey(ServiceBranch, on_delete=models.PROTECT, related_name="veterans")
    rank = models.ForeignKey(Rank, on_delete=models.PROTECT, related_name="veterans")
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)

    # Contact & location
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    state = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)

    # Service related
    date_of_enrolment = models.DateField(null=True, blank=True)
    date_of_discharge = models.DateField(null=True, blank=True)
    total_service_years = models.PositiveIntegerField(null=True, blank=True)
    last_unit_served = models.CharField(max_length=255, blank=True)

    # Status for verification
    verification_status = models.CharField(
        max_length=30,
        choices=SERVICE_STATUS_CHOICES,
        default="PENDING_VERIFICATION",
    )
    verification_notes = models.TextField(blank=True)

    # For portal login (optional now, can be used later)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="veteran_profile",
        help_text="Optional link to auth user (for candidate portal).",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["branch", "rank__order", "last_name", "first_name"]

    def __str__(self):
        return f"{self.service_number} - {self.rank} {self.first_name} {self.last_name}"


class Vacancy(models.Model):
    """
    Vacancy for a veteran post (PI Staff, CVDO, etc.) at a specific NCC organization.
    """
    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("PUBLISHED", "Published"),
        ("CLOSED", "Closed"),
    ]

    title = models.CharField(max_length=255, help_text="e.g. PI Staff (Army), CVDO (Contractual)")
    description = models.TextField()
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="vacancies",
        help_text="NCC Unit / Group / Dte where the veteran will be employed.",
    )
    branch = models.ForeignKey(
        ServiceBranch,
        on_delete=models.PROTECT,
        related_name="vacancies",
        help_text="Service of veteran required for this vacancy.",
    )
    allowed_ranks = models.ManyToManyField(
        Rank,
        blank=True,
        help_text="If only certain ranks are allowed for this vacancy.",
        related_name="vacancies",
    )

    sanctioned_strength = models.PositiveIntegerField(
        default=1,
        help_text="Total sanctioned posts for this vacancy type at this organization.",
    )
    current_hired = models.PositiveIntegerField(
        default=0,
        help_text="Number of veterans already hired here.",
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")
    opening_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vacancies_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-opening_date", "title"]

    def __str__(self):
        return f"{self.title} @ {self.organization}"

    @property
    def remaining_slots(self):
        return max(self.sanctioned_strength - self.current_hired, 0)


class Application(models.Model):
    """
    Application of a veteran to a specific vacancy, with pipeline stages.
    """
    STATUS_CHOICES = [
        ("APPLIED", "Applied"),
        ("UNDER_SCRUTINY", "Under Scrutiny"),
        ("SHORTLISTED", "Shortlisted"),
        ("INTERVIEW_SCHEDULED", "Interview Scheduled"),
        ("RECOMMENDED", "Recommended"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("WITHDRAWN", "Withdrawn"),
    ]

    veteran = models.ForeignKey(Veteran, on_delete=models.CASCADE, related_name="applications")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")

    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="APPLIED")
    remarks = models.TextField(blank=True)

    # For audit trail (which HQ changed status etc.)
    last_updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="applications_updated",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("veteran", "vacancy")
        ordering = ["-application_date"]

    def __str__(self):
        return f"{self.veteran} -> {self.vacancy} ({self.status})"


class Registration(models.Model):
    """
    Simple public registration record.
    Later we can link this to Veteran or User models.
    """
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"

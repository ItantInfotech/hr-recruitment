from django.contrib import admin
from .models import (
    ServiceBranch,
    Rank,
    Organization,
    Veteran,
    Vacancy,
    Application,
)


@admin.register(ServiceBranch)
class ServiceBranchAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name")
    search_fields = ("name", "short_name")


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ("name", "abbreviation", "branch", "order")
    list_filter = ("branch",)
    search_fields = ("name", "abbreviation")


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "parent")
    list_filter = ("type",)
    search_fields = ("name",)


@admin.register(Veteran)
class VeteranAdmin(admin.ModelAdmin):
    list_display = (
        "service_number",
        "branch",
        "rank",
        "first_name",
        "last_name",
        "verification_status",
        "state",
        "district",
        "created_at",
    )
    list_filter = ("branch", "rank", "verification_status", "state")
    search_fields = ("service_number", "first_name", "last_name", "email", "phone")


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "organization",
        "branch",
        "sanctioned_strength",
        "current_hired",
        "status",
        "opening_date",
        "closing_date",
    )
    list_filter = ("status", "branch", "organization__type")
    search_fields = ("title", "organization__name")
    filter_horizontal = ("allowed_ranks",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "veteran",
        "vacancy",
        "status",
        "application_date",
        "updated_at",
        "last_updated_by",
    )
    list_filter = ("status", "vacancy__organization__type", "vacancy__branch")
    search_fields = (
        "veteran__service_number",
        "veteran__first_name",
        "veteran__last_name",
        "vacancy__title",
    )

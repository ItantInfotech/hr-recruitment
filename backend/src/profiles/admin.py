from django.contrib import admin
from .models import JobApplication


from django.contrib import admin
from .models import CandidateProfile, Education, Experience, Job, JobApplication

class EducationInline(admin.TabularInline):
    model = Education
    extra = 0

class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'mobile', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'mobile', 'id_doc_number')
    inlines = [EducationInline, ExperienceInline]

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'posted_on')
    search_fields = ('title', 'company', 'location')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'applied_on', 'status')
    list_filter = ('status',)
    search_fields = ('candidate__first_name', 'candidate__last_name', 'job__title')


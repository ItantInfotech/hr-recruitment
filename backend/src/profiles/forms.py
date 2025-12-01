from django import forms
from .models import CandidateProfile, Education, Experience, JobApplication
from django.forms import inlineformset_factory

class CandidateProfileForm(forms.ModelForm):
    computer_proficiency_text = forms.CharField(required=False, help_text="Comma separated")
    languages_known_text = forms.CharField(required=False, help_text="Comma separated")

    class Meta:
        model = CandidateProfile
        exclude = ['user', 'created_at', 'updated_at', 'computer_proficiency', 'languages_known']

    def clean(self):
        cleaned = super().clean()
        cp = cleaned.get('computer_proficiency_text', '')
        ln = cleaned.get('languages_known_text', '')
        cleaned['computer_proficiency'] = [x.strip() for x in cp.split(',') if x.strip()] if cp else []
        cleaned['languages_known'] = [x.strip() for x in ln.split(',') if x.strip()] if ln else []
        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.computer_proficiency = self.cleaned_data.get('computer_proficiency', [])
        obj.languages_known = self.cleaned_data.get('languages_known', [])
        if commit:
            obj.save()
        return obj

EducationFormSet = inlineformset_factory(
    CandidateProfile, Education,
    fields=['degree', 'university', 'start_date', 'end_date', 'percentage', 'certificate'],
    extra=1, can_delete=True
)

ExperienceFormSet = inlineformset_factory(
    CandidateProfile, Experience,
    fields=['from_date', 'to_date', 'organization', 'designation', 'responsibilities', 'experience_proof'],
    extra=1, can_delete=True
)

class JobApplyForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['remarks']

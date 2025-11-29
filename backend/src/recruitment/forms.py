from django import forms
from captcha.fields import CaptchaField

class RegistrationForm(forms.Form):
    full_name = forms.CharField(
        max_length=255,
        label="Full Name",
        widget=forms.TextInput(attrs={"placeholder": "Your full name"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com"}),
    )
    confirm_email = forms.EmailField(
        label="Confirm Email",
        widget=forms.EmailInput(attrs={"placeholder": "Repeat your email"}),
    )
    phone = forms.CharField(
        max_length=20,
        label="Phone Number",
        widget=forms.TextInput(attrs={"placeholder": "10-digit mobile number"}),
    )
    otp = forms.CharField(
        max_length=10,
        label="OTP",
        help_text="Dummy for now – enter 1234.",
        widget=forms.TextInput(attrs={"placeholder": "1234"}),
    )

    # 🔒 Real image-based CAPTCHA field
    captcha = CaptchaField(label="Enter the text from the image")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")

        if email and confirm_email and email != confirm_email:
            self.add_error("confirm_email", "Email addresses do not match.")

        return cleaned_data
    

class CandidateLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com"}),
    )
    phone = forms.CharField(
        label="Phone Number",
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "10-digit mobile number"}),
    )
    otp = forms.CharField(
        label="One-Time Password",
        max_length=10,
        widget=forms.TextInput(attrs={"placeholder": "Enter OTP (use 1234 for demo)"}),
    )
    captcha = CaptchaField(label="Security Check")

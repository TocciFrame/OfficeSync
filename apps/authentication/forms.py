from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from apps.user_profile.models import Profile

# Regex enforcing YY-XXXX-XXX format (e.g. 24-0527-622)
school_id_regex = RegexValidator(
    regex=r'^\d{2}-\d{4}-\d{3}$',
    message="School ID must follow the format YY-XXXX-XXX (e.g., 24-0527-622)."
)

ROLE_CHOICES = [
    ('student', 'Student'),
    ('faculty', 'Faculty'),
]
    
DEPARTMENT_CHOICES = [
    ('CCS', 'College of Computer Studies'),
    ('CEA', 'College of Engineering and Architecture'),
    ('CASE', 'College of Arts, Sciences, and Education'),
    ('CMBA', 'College of Management, Business, and Accountancy'),
    ('CCJ', 'College of Criminal Justice'),
    ('CNAHS', 'College of Nursing and Allied Health Sciences'),
]

class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-input'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-input'})
    )
    school_id = forms.CharField(
        validators=[school_id_regex],
        widget=forms.TextInput(attrs={'placeholder': 'XX-XXXX-XXX', 'class': 'form-input'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'you@university.edu', 'class': 'form-input'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-input'})
    )
    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.HiddenInput(attrs={'id': 'id_role'}),
        initial='student'
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'class': 'form-input'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_school_id(self):
        school_id = self.cleaned_data.get('school_id')
        if Profile.objects.filter(school_id__iexact=school_id).exists():
            raise forms.ValidationError("School ID is already registered.")
        return school_id

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email address is already registered.")
        return email

class LoginForm(forms.Form):
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.HiddenInput(attrs={'id': 'id_role'}),
        initial='student'
    )
    email_or_school_id = forms.CharField(
        label="Institutional Email / School ID#",
        widget=forms.TextInput(attrs={
            'placeholder': 'you@university.edu or 24-0527-622',
            'class': 'form-input'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'form-input'
        })
    )
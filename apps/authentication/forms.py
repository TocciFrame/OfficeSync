from django import forms
from django.contrib.auth import get_user_model
from apps.user_profile.models import DEPARTMENT_CHOICES, StudentProfile, FacultyProfile

class LoginForm(forms.Form):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.HiddenInput(),
        initial='student'
    )
    email_or_school_id = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Email or School ID#',
            'class': 'form-input'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password',
            'class': 'form-input'
        })
    )


class RegisterForm(forms.Form):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.HiddenInput(),
        initial='student'
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-input'})
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-input'})
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-input'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Institutional Email', 'class': 'form-input'})
    )
    school_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'School ID (YY-XXXX-XXX)', 'class': 'form-input'})
    )
    department = forms.ChoiceField(
        choices=[('', 'Select Department')] + DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-input'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-input'})
    )

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if get_user_model().objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("That username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_school_id(self):
        school_id = self.cleaned_data['school_id'].strip()
        if (StudentProfile.objects.filter(school_id__iexact=school_id).exists() or
                FacultyProfile.objects.filter(school_id__iexact=school_id).exists()):
            raise forms.ValidationError("This School ID is already registered.")
        return school_id

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data
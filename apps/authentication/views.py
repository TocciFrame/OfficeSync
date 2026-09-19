from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from apps.user_profile.models import Profile
from .forms import RegistrationForm, LoginForm

def login_view(request):
    # Redirect already logged-in users directly to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['email_or_school_id'].strip()
            password = form.cleaned_data['password']
            selected_role = form.cleaned_data['role']

            user_obj = None

            if '@' in identifier:
                try:
                    user_obj = User.objects.get(email__iexact=identifier)
                except User.DoesNotExist:
                    user_obj = None
            else:
                try:
                    profile = Profile.objects.get(school_id__iexact=identifier)
                    user_obj = profile.user
                except Profile.DoesNotExist:
                    user_obj = None

            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)
            else:
                user = None

            if user is not None:
                profile, _ = Profile.objects.get_or_create(user=user)

                if profile.role == selected_role or user.is_superuser:
                    login(request, user)
                    return redirect('dashboard:dashboard') # Target route
                else:
                    role_display = "Student" if selected_role == "student" else "Faculty"
                    messages.error(request, f"This account is not registered as a {role_display}.")
            else:
                messages.error(request, "Invalid Email / School ID# or password.")
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            school_id = form.cleaned_data['school_id']
            role = form.cleaned_data['role']
            department = form.cleaned_data['department']

            # 1. Create Django User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # 2. Save extended profile details
            Profile.objects.create(
                user=user,
                school_id=school_id,
                role=role,
                department=department
            )

            messages.success(request, "Account created successfully! Please sign in.")
            return redirect('authentication:login')
    else:
        form = RegistrationForm()

    return render(request, 'authentication/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('authentication:login')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from apps.user_profile.models import StudentProfile, FacultyProfile
from .forms import LoginForm, RegisterForm

User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['email_or_school_id'].strip()
            password = form.cleaned_data['password']
            selected_role = form.cleaned_data['role']

            user_obj = None

            # Resolve user by Email or School ID
            if '@' in identifier:
                try:
                    user_obj = User.objects.get(email__iexact=identifier)
                except User.DoesNotExist:
                    user_obj = None
            else:
                if selected_role == 'student':
                    try:
                        student_profile = StudentProfile.objects.get(school_id__iexact=identifier)
                        user_obj = student_profile.user
                    except StudentProfile.DoesNotExist:
                        user_obj = None
                else:
                    try:
                        faculty_profile = FacultyProfile.objects.get(school_id__iexact=identifier)
                        user_obj = faculty_profile.user
                    except FacultyProfile.DoesNotExist:
                        user_obj = None

            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)
            else:
                user = None

            if user is not None:
                has_student_profile = hasattr(user, 'student_profile')
                has_faculty_profile = hasattr(user, 'faculty_profile')

                is_valid_role = (selected_role == 'student' and has_student_profile) or \
                                (selected_role == 'faculty' and has_faculty_profile)

                if is_valid_role:
                    login(request, user)
                    return redirect('dashboard:dashboard')
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
        form = RegisterForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']

            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )

            if role == 'student':
                StudentProfile.objects.create(
                    user=user,
                    school_id=form.cleaned_data['school_id'],
                    department=form.cleaned_data['department']
                )
            else:
                FacultyProfile.objects.create(
                    user=user,
                    school_id=form.cleaned_data['school_id'],
                    department=form.cleaned_data['department']
                )

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('authentication:login')
    else:
        form = RegisterForm()

    return render(request, 'authentication/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('authentication:login')
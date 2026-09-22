from django.shortcuts import render, redirect
from apps.user_profile.models import FacultyProfile, DEPARTMENT_CHOICES

def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    faculty_count = FacultyProfile.objects.count()
    department_count = len(DEPARTMENT_CHOICES)

    context = {
        'faculty_count': faculty_count,
        'department_count': department_count,
    }
    return render(request, 'landing/landing.html', context)
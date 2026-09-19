from django.shortcuts import render, redirect
from apps.user_profile.models import Profile

# Create your views here.
def landing_view(request):
    # 1. Redirect authenticated users to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    # 2. Count registered faculty accounts
    faculty_count = Profile.objects.filter(role__iexact='faculty').count()

    # 3. Total defined departments in the system
    department_count = len(Profile.DEPARTMENT_CHOICES)

    context = {
        'faculty_count': faculty_count,
        'department_count': department_count,
    }

    return render(request, 'landing/landing.html', context)
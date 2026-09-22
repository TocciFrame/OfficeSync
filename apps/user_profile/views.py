from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile_view(request):
    user = request.user
    is_faculty = hasattr(user, 'faculty_profile')
    profile = getattr(user, 'faculty_profile', None) if is_faculty else getattr(user, 'student_profile', None)
    message = None

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.save()
        message = "Profile updated successfully!"

    # The template displays a read-only "role" field; attach it for display only
    # (it isn't a stored field, since role is already determined by profile type).
    if profile is not None:
        profile.role = 'Faculty' if is_faculty else 'Student'

    context = {
        'is_faculty': is_faculty,
        'profile': profile,
        'message': message,
    }
    return render(request, 'user_profile/profile.html', context)
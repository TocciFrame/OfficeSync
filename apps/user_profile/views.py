from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    message = None

    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name", "")
        request.user.last_name = request.POST.get("last_name", "")
        request.user.email = request.POST.get("email", "")
        request.user.save()

        profile.role = request.POST.get("role", "")
        profile.bio = request.POST.get("bio", "")
        profile.save()
        message = "Profile updated successfully!"

    return render(request, "user_profile/profile.html", {"profile": profile, "message": message})
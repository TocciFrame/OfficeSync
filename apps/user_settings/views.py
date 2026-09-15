from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserSettings

# Create your views here.
@login_required
def settings_view(request):
    settings_obj, _ = UserSettings.objects.get_or_create(user=request.user)
    message = None

    if request.method == "POST":
        settings_obj.dark_mode = request.POST.get("dark_mode") == "on"
        settings_obj.email_notif = request.POST.get("email_notif") == "on"
        settings_obj.save()
        message = "Settings saved successfully!"

    return render(request, "user_settings/settings.html", {
        "settings": settings_obj,
        "message": message
    })

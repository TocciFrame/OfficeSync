from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from apps.user_profile.models import Profile

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard:home")
        return render(request, "authentication/login.html", {
            "error": "Invalid username or password."
        })
    return render(request, "authentication/login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password")
        role = request.POST.get("role", "")

        if User.objects.filter(username=username).exists():
            return render(request, "authentication/register.html", {
                "error": "Username already exists."
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        Profile.objects.create(
            user=user,
            role=role
        )

        return redirect("authentication:login")

    return render(request, "authentication/register.html")

def logout_view(request):
    logout(request)
    return redirect("authentication:login")
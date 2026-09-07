from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import OfficeSyncRegistrationForm  

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = OfficeSyncRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = OfficeSyncRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
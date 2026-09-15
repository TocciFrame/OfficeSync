from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FacultyStatus

@login_required
def home_view(request):
    if request.method == "POST" and (request.user.is_staff or request.user.is_superuser):
        status_obj, _ = FacultyStatus.objects.get_or_create(user=request.user)
        status_obj.status = request.POST.get("status", status_obj.status)
        status_obj.room_number = request.POST.get("room_number", status_obj.room_number)
        status_obj.back_at = request.POST.get("back_at", "")
        status_obj.save()
        return redirect("dashboard:home")

    query = request.GET.get("q", "")
    faculty_list = FacultyStatus.objects.select_related('user').all()

    if query:
        faculty_list = faculty_list.filter(
            user__first_name__icontains=query
        ) | faculty_list.filter(
            user__last_name__icontains=query
        ) | faculty_list.filter(
            department__icontains=query
        )

    my_status = None
    if request.user.is_staff or request.user.is_superuser:
        my_status, _ = FacultyStatus.objects.get_or_create(user=request.user)

    context = {
        "faculty_list": faculty_list,
        "my_status": my_status,
        "query": query,
    }
    return render(request, "dashboard/home.html", context)
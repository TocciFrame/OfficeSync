from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import FacultyStatus


@login_required
def dashboard_view(request):
    # If the logged-in user is faculty, make sure they have a live status row
    my_status = None
    if hasattr(request.user, 'faculty_profile'):
        faculty_profile = request.user.faculty_profile
        my_status, _ = FacultyStatus.objects.get_or_create(
            user=request.user,
            defaults={
                'room_number': '',
            }
        )

    # Only staff/superusers can push a status update from the admin panel
    if request.method == 'POST' and (request.user.is_staff or request.user.is_superuser) and my_status:
        my_status.status = request.POST.get('status', my_status.status)
        my_status.room_number = request.POST.get('room_number', my_status.room_number)
        my_status.back_at = request.POST.get('back_at', '').strip()
        my_status.save()

    # Live search across the master status grid
    query = request.GET.get('q', '').strip()
    faculty_list = FacultyStatus.objects.select_related('user').all().order_by('user__last_name', 'user__first_name')
    if query:
        faculty_list = faculty_list.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(department__icontains=query)
        )

    context = {
        'faculty_list': faculty_list,
        'my_status': my_status,
        'query': query,
    }
    return render(request, 'dashboard/home.html', context)
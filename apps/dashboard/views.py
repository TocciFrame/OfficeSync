from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.user_profile.models import FacultyProfile
from .models import FacultyStatus

@login_required
def dashboard_view(request):
    # 1. Fetch or create faculty profile for logged in user
    faculty_profile, _ = FacultyProfile.objects.get_or_create(user=request.user)

    # 2. Fetch or create current user status
    my_status, _ = FacultyStatus.objects.get_or_create(
        faculty=faculty_profile,
        defaults={
            'room_number': faculty_profile.office_room or '',
            'status': 'OUT'
        }
    )

    # 3. Handle POST status updates
    if request.method == 'POST':
        new_status = request.POST.get('status')
        new_room = request.POST.get('room_number')
        new_back_at = request.POST.get('back_at')

        if new_status:
            my_status.status = new_status
        if new_room is not None:
            my_status.room_number = new_room
        if new_back_at is not None:
            my_status.back_at = new_back_at

        my_status.save()
        return redirect('dashboard:dashboard')

    # 4. Fetch all active faculty status records to display on board
    faculty_list = (
        FacultyStatus.objects.select_related('faculty__user')
        .all()
        .order_by('faculty__user__last_name', 'faculty__user__first_name')
    )

    context = {
        'my_status': my_status,
        'faculty_profile': faculty_profile,
        'faculty_list': faculty_list,
        'status_choices': FacultyStatus.STATUS_CHOICES,
    }
    return render(request, 'dashboard/home.html', context)
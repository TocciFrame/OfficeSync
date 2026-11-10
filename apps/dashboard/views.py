from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from apps.user_profile.models import FacultyProfile, StudentProfile
from .models import FacultyStatus

@login_required
def dashboard_view(request):
    # 1. Strict Role Determination: Default to Student unless strictly Faculty
    has_student_profile = StudentProfile.objects.filter(user=request.user).exists()
    has_faculty_profile = FacultyProfile.objects.filter(user=request.user).exists()

    if has_student_profile:
        is_faculty = False
    elif has_faculty_profile:
        is_faculty = True
    else:
        # Default fallback for regular users: Student
        is_faculty = False

    my_status = None
    faculty_profile = None

    # 2. FACULTY-ONLY LOGIC: Status panel is only accessible to Faculty accounts
    if is_faculty:
        faculty_profile = FacultyProfile.objects.get(user=request.user)
        my_status, _ = FacultyStatus.objects.get_or_create(
            faculty=faculty_profile,
            defaults={
                'room_number': getattr(faculty_profile, 'office_room', '') or '',
                'status': 'OUT'
            }
        )

        # Handle POST status updates (Faculty only)
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

    # 3. LIVE BOARD DATA: Auto-create missing status entries for registered Faculty members
    all_faculty = FacultyProfile.objects.select_related('user').all()
    for fp in all_faculty:
        FacultyStatus.objects.get_or_create(
            faculty=fp,
            defaults={
                'room_number': getattr(fp, 'office_room', '') or '',
                'status': 'OUT'
            }
        )

    # 4. Fetch faculty status list for the live board
    query = request.GET.get('q', '').strip()
    faculty_list = FacultyStatus.objects.select_related('faculty__user', 'faculty').all()

    if query:
        faculty_list = faculty_list.filter(
            Q(faculty__user__first_name__icontains=query) |
            Q(faculty__user__last_name__icontains=query) |
            Q(faculty__user__username__icontains=query) |
            Q(faculty__department__icontains=query)
        )

    faculty_list = faculty_list.order_by('faculty__user__last_name', 'faculty__user__first_name')

    context = {
        'is_faculty': is_faculty,
        'my_status': my_status,
        'faculty_profile': faculty_profile,
        'faculty_list': faculty_list,
        'status_choices': FacultyStatus.STATUS_CHOICES,
        'query': query,
    }

    return render(request, 'dashboard/home.html', context)
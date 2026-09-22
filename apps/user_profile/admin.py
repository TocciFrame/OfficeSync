from django.contrib import admin
from .models import StudentProfile, FacultyProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school_id', 'department')
    search_fields = ('user__username', 'user__email', 'school_id', 'department')
    list_filter = ('department',)


@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school_id', 'department', 'office_room', 'office_hours')
    search_fields = ('user__username', 'user__email', 'school_id', 'department', 'office_room')
    list_filter = ('department',)
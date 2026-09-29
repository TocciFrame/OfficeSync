from django.db import models
from apps.user_profile.models import FacultyProfile

class FacultyStatus(models.Model):
    STATUS_CHOICES = [
        ('IN_OFFICE', 'In-Office'),
        ('IN_CLASS', 'In-Class'),
        ('ON_BREAK', 'On-Break'),
        ('OUT', 'Out of Office'),
    ]

    faculty = models.OneToOneField(
        FacultyProfile, 
        on_delete=models.CASCADE, 
        related_name='status_record', 
        db_column='faculty_id'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OUT')
    room_number = models.CharField(
        max_length=50, 
        blank=True, 
        db_column='room_number'
    )
    back_at = models.CharField(max_length=50, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dashboard_faculty_status'

    def __str__(self):
        return f"{self.faculty.user.get_full_name() or self.faculty.user.username} - {self.status}"
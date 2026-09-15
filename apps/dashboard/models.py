from django.db import models
from django.contrib.auth.models import User

class FacultyStatus(models.Model):
    STATUS_CHOICES = [
        ('IN_OFFICE', 'In-Office'),
        ('IN_CLASS', 'In-Class'),
        ('ON_BREAK', 'On-Break'),
        ('OUT', 'Out of Office'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_status')
    department = models.CharField(max_length=100, default="Computer Science")
    room_number = models.CharField(max_length=20, default="Room 101")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OUT')
    back_at = models.CharField(max_length=50, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.status}"
from django.db import models
from django.conf import settings

DEPARTMENT_CHOICES = [
    ('CCS', 'College of Computer Studies'),
    ('CEA', 'College of Engineering and Architecture'),
    ('CASE', 'College of Arts, Sciences, and Education'),
    ('CMBA', 'College of Management, Business, and Accountancy'),
    ('CCJ', 'College of Criminal Justice'),
    ('CNAHS', 'College of Nursing and Allied Health Sciences'),
]

class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    school_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"[Student] {self.user.username} ({self.school_id})"


class FacultyProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='faculty_profile'
    )
    school_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    office_room = models.CharField(max_length=20, blank=True, null=True)
    office_hours = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"[Faculty] {self.user.username} ({self.school_id})"
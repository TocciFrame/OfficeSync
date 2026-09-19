from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    ]

    DEPARTMENT_CHOICES = [
        ('CCS', 'College of Computer Studies'),
        ('CEA', 'College of Engineering and Architecture'),
        ('CASE', 'College of Arts, Sciences, and Education'),
        ('CMBA', 'College of Management, Business, and Accountancy'),
        ('CCJ', 'College of Criminal Justice'),
        ('CNAHS', 'College of Nursing and Allied Health Sciences'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    school_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.school_id}) - {self.role}"
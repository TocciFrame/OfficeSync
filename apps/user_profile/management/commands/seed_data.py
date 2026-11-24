"""
Wipe the test data and populate the database with fresh, formatted accounts.

Usage:
    python manage.py seed_data                      # 10 faculty + 10 students
    python manage.py seed_data --faculty 5 --students 20
    python manage.py seed_data --noinput            # skip the confirmation prompt

Faculty : first name "Professor", last name 1, 2, 3 ...  password FAC00001, FAC00002 ...
Student : first name "Student",   last name 1, 2, 3 ...  password STUD00001, STUD00002 ...
School ID format: xx-xxxx-xxx, starting at 00-0000-001 (one sequence per role).
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.db import connection, transaction

from apps.dashboard.models import FacultyStatus
from apps.user_profile.models import (
    DEPARTMENT_CHOICES, FacultyProfile, StudentProfile,
)
from apps.user_settings.models import UserSettings

User = get_user_model()


def make_school_id(n):
    """1 -> 00-0000-001, 1000 -> 00-0001-000 (xx-xxxx-xxx)."""
    return f"00-{n // 1000:04d}-{n % 1000:03d}"


class Command(BaseCommand):
    help = "Delete test data and seed formatted Faculty and Student accounts."

    def add_arguments(self, parser):
        parser.add_argument('--faculty', type=int, default=10, help='Number of faculty (default 10)')
        parser.add_argument('--students', type=int, default=10, help='Number of students (default 10)')
        parser.add_argument('--noinput', action='store_true', help='Do not ask for confirmation')

    def handle(self, *args, **opts):
        n_fac, n_stu = opts['faculty'], opts['students']
        if n_fac < 0 or n_stu < 0:
            raise CommandError("Counts must be zero or greater.")

        if not opts['noinput']:
            self.stdout.write(self.style.WARNING(
                "This will DELETE all users (except superusers), their profiles, "
                "faculty statuses and settings, then create "
                f"{n_fac} faculty and {n_stu} students."))
            if input("Type 'yes' to continue: ").strip().lower() != 'yes':
                self.stdout.write("Cancelled.")
                return

        with transaction.atomic():
            self._wipe()
            self._reset_sequences()
            self._seed_faculty(n_fac)
            self._seed_students(n_stu)

        self.stdout.write(self.style.SUCCESS(
            f"Done: {n_fac} faculty and {n_stu} students created."))

    # ---------------------------------------------------------------- wipe
    def _wipe(self):
        # Child tables first (explicit), then users. Superusers are kept so
        # you do not lose access to /admin/.
        FacultyStatus.objects.all().delete()
        UserSettings.objects.all().delete()
        FacultyProfile.objects.all().delete()
        StudentProfile.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write("Old test data removed.")

    def _reset_sequences(self):
        # Make the auto-increment ids start again from the lowest free number.
        # no_style() is required: the colored terminal style injects ANSI
        # escape codes into the SQL and PostgreSQL rejects it.
        models = [User, FacultyProfile, StudentProfile, FacultyStatus, UserSettings]
        sql_list = connection.ops.sequence_reset_sql(no_style(), models)
        with connection.cursor() as cursor:
            for sql in sql_list:
                cursor.execute(sql)

    # ---------------------------------------------------------------- seed
    def _seed_faculty(self, count):
        depts = [code for code, _ in DEPARTMENT_CHOICES]
        statuses = ['IN_OFFICE', 'IN_CLASS', 'ON_BREAK', 'OUT']
        back_times = {'IN_OFFICE': '', 'IN_CLASS': '10:30 AM',
                      'ON_BREAK': '1:00 PM', 'OUT': '3:00 PM'}

        for i in range(1, count + 1):
            user = User.objects.create_user(
                username=f"professor{i}",
                email=f"professor{i}@officesync.test",
                password=f"FAC{i:05d}",
                first_name="Professor",
                last_name=str(i),
            )
            room = f"Rm {100 + i}"
            profile = FacultyProfile.objects.create(
                user=user,
                school_id=make_school_id(i),
                department=depts[(i - 1) % len(depts)],
                office_room=room,
                office_hours="Mon-Fri 9:00 AM - 12:00 PM",
            )
            status = statuses[(i - 1) % len(statuses)]
            FacultyStatus.objects.create(
                faculty=profile,
                status=status,
                room_number=room,
                back_at=back_times[status] or None,
            )
            UserSettings.objects.create(user=user)

    def _seed_students(self, count):
        depts = [code for code, _ in DEPARTMENT_CHOICES]

        for i in range(1, count + 1):
            user = User.objects.create_user(
                username=f"student{i}",
                email=f"student{i}@officesync.test",
                password=f"STUD{i:05d}",
                first_name="Student",
                last_name=str(i),
            )
            StudentProfile.objects.create(
                user=user,
                school_id=make_school_id(i),
                department=depts[(i - 1) % len(depts)],
            )
            UserSettings.objects.create(user=user)
# pages/management/commands/populate_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Populate the database with 5 instructors, 60 students, plus 3 pending users."

    def handle(self, *args, **kwargs):
        # 5 instructors
        for i in range(1, 6):
            username = f"instructor{i}"
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    email=f"{username}@courpera.com",
                    password="password123",
                    role=User.TEACHER,
                    first_name=f"Instructor{i}",
                    last_name="Test"
                )
                self.stdout.write(self.style.SUCCESS(f"Created instructor: {username}"))
            else:
                self.stdout.write(self.style.WARNING(f"Instructor {username} already exists."))

        # 60 students
        for i in range(1, 61):
            username = f"student{i}"
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    email=f"{username}@courpera.com",
                    password="password123",
                    role=User.STUDENT,
                    first_name=f"Student{i}",
                    last_name="Test"
                )
                self.stdout.write(self.style.SUCCESS(f"Created student: {username}"))
            else:
                self.stdout.write(self.style.WARNING(f"Student {username} already exists."))

        # 3 pending users (2 want to be student, 1 wants to be instructor)
        # We'll store them with is_active=False
        pending_users = [
            ("pending_student1", "student"),
            ("pending_student2", "student"),
            ("pending_instructor1", "teacher"),
        ]
        for (uname, role) in pending_users:
            if not User.objects.filter(username=uname).exists():
                user = User.objects.create_user(
                    username=uname,
                    email=f"{uname}@courpera.com",
                    password="password123",
                    role=role
                )
                user.is_active = False  # pending approval
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created pending user: {uname} (role={role})"))
            else:
                self.stdout.write(self.style.WARNING(f"Pending user {uname} already exists."))

        self.stdout.write(self.style.SUCCESS("User population complete (instructors, students, pending users)."))

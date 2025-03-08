from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Populate the database with 5 instructors and 60 students."

    def handle(self, *args, **kwargs):
        # Create 5 instructors
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

        # Create 60 students
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

        self.stdout.write(self.style.SUCCESS("User population complete."))

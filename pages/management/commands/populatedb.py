from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with 90 users (80 students and 10 instructors) and sample courses.'

    def handle(self, *args, **kwargs):
        # Create instructors
        instructors = []
        for i in range(1, 11):  # 10 instructors
            username = f"instructor{i}"
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f"{username}@courpera.com",
                    password="password123",
                    role=User.TEACHER,
                    first_name=f"Instructor{i}",
                    last_name="Test"
                )
                instructors.append(user)
                self.stdout.write(self.style.SUCCESS(f"Created instructor: {username}"))
            else:
                user = User.objects.get(username=username)
                instructors.append(user)
                self.stdout.write(self.style.WARNING(f"Instructor {username} already exists."))

        # Create students
        for i in range(1, 81):  # 80 students
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

        # Create courses: Each instructor gets 3 courses
        course_counter = 1
        for instructor in instructors:
            for j in range(1, 4):  # 3 courses per instructor
                course_name = f"Course {course_counter}: Introduction to Subject {course_counter}"
                if not Course.objects.filter(title=course_name).exists():
                    Course.objects.create(
                        title=course_name,
                        description=f"This is a sample description for {course_name}.",
                        teacher=instructor,
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created course: {course_name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Course {course_name} already exists."))
                course_counter += 1

        self.stdout.write(self.style.SUCCESS("Database population complete."))

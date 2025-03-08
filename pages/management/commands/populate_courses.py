import random
from django.core.management.base import BaseCommand
from courses.models import Course, CourseInstance
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate 10 courses and 3 course instances for each course offering in specified semesters.'

    def handle(self, *args, **kwargs):
        course_names = ["CM1005", "CM1015", "CM1035", "CM1050", "CM2010", "CM2020", "CM2045", "CM3005", "CM3015", "CM3060"]
        courses = []
        for name in course_names:
            course, created = Course.objects.get_or_create(name=name, defaults={'description': f"Description for {name}."})
            courses.append(course)
            if created:
                self.stdout.write(f"Created course: {name}")
            else:
                self.stdout.write(f"Course {name} already exists.")
        
        semesters = [
            {'name': 'Spring 2024', 'start_date': date(2024, 4, 1), 'end_date': date(2024, 9, 30)},
            {'name': 'Autumn 2024', 'start_date': date(2024, 10, 1), 'end_date': date(2025, 3, 31)},
            {'name': 'Spring 2025', 'start_date': date(2025, 4, 1), 'end_date': date(2025, 9, 30)},
        ]

        instructors = list(User.objects.filter(role=User.TEACHER)[:5])
        if len(instructors) < 5:
            self.stdout.write("Error: Not enough instructors. Need at least 5.")
            return

        for course in courses:
            for sem in semesters:
                instance, created = CourseInstance.objects.get_or_create(
                    course=course,
                    semester=sem['name'],
                    defaults={
                        'start_date': sem['start_date'],
                        'end_date': sem['end_date'],
                        'instructor': random.choice(instructors),
                    }
                )
                instance.update_status()
                if created:
                    self.stdout.write(f"Created instance for {course.name} - {sem['name']}")
                else:
                    self.stdout.write(f"Instance for {course.name} - {sem['name']} already exists.")

        self.stdout.write("Course population complete.")

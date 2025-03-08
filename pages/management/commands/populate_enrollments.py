import random
from django.core.management.base import BaseCommand
from courses.models import CourseInstance, Enrollment
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Enroll each of the 60 students in 4 random course instances per semester, with a max of 30 enrollments per instance.'

    def handle(self, *args, **kwargs):
        students = list(User.objects.filter(role=User.STUDENT)[:60])
        if len(students) < 60:
            self.stdout.write("Error: Not enough students. Need at least 60.")
            return

        semesters = ['Spring 2024', 'Autumn 2024', 'Spring 2025']
        for semester in semesters:
            instances = list(CourseInstance.objects.filter(semester=semester))
            for student in students:
                enrollment_count = Enrollment.objects.filter(student=student, course_instance__semester=semester).count()
                if enrollment_count < 4:
                    needed = 4 - enrollment_count
                    random.shuffle(instances)
                    for inst in instances:
                        if Enrollment.objects.filter(student=student, course_instance=inst).exists():
                            continue
                        if inst.enrollments.count() < 30:
                            Enrollment.objects.create(student=student, course_instance=inst)
                            needed -= 1
                            self.stdout.write(f"Enrolled {student.username} in {inst}")
                            if needed == 0:
                                break
        self.stdout.write("Enrollment population complete.")

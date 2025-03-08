from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from courses.models import Course
from users.models import User

@shared_task
def send_enrollment_email(course_id, student_id):
    try:
        course = Course.objects.get(id=course_id)
        student = User.objects.get(id=student_id)
        teacher = course.teacher

        subject = f"New Enrollment in {course.title}"
        message = (
            f"Hello {teacher.username},\n\n"
            f"Student {student.username} has enrolled in your course: {course.title}.\n\n"
            "Regards,\nYour eLearning Platform"
        )
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
        recipient_list = [teacher.email]
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f"Error sending enrollment email: {e}")

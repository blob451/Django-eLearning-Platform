from django.db import models
from django.conf import settings
from django.utils import timezone

# Course model
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='courses',
        help_text="The teacher (User with role 'teacher') who created the course."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

# Enrollment model: linking students to courses
class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='enrollments',
        help_text="Student enrolling in the course."
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='enrollments'
    )
    enrolled_on = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True, help_text="Indicates if enrollment is active.")

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

# Feedback model: for students to leave feedback on courses
class Feedback(models.Model):
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='feedbacks'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='feedbacks'
    )
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Optional rating")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.course.title}"

# StatusUpdate model: for posting status updates on a user's home page
class StatusUpdate(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='status_updates'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status by {self.user.username} at {self.timestamp}"

# CourseMaterial model: for uploading course files/materials
class CourseMaterial(models.Model):
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='materials'
    )
    file = models.FileField(upload_to='course_materials/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Material for {self.course.title}"

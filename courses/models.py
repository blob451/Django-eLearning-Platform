from django.db import models
from django.conf import settings
from django.utils import timezone

class Course(models.Model):
    # Updated: Set a default value for name so that migrations don't require a one-off default
    name = models.CharField(max_length=20, unique=True, default="TBD")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class CourseInstance(models.Model):
    SEMESTER_CHOICES = [
        ('Spring 2024', 'Spring 2024'),
        ('Autumn 2024', 'Autumn 2024'),
        ('Spring 2025', 'Spring 2025'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Past', 'Past'),
        ('Upcoming', 'Upcoming'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='instances')
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='course_instances')

    def __str__(self):
        return f"{self.course.name} - {self.semester}"

    def update_status(self):
        today = timezone.now().date()
        if self.start_date <= today <= self.end_date:
            self.status = 'Active'
        elif today > self.end_date:
            self.status = 'Past'
        elif today < self.start_date:
            self.status = 'Upcoming'
        self.save()

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course_instance = models.ForeignKey(CourseInstance, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_on = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('student', 'course_instance')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course_instance}"

class Feedback(models.Model):
    course_instance = models.ForeignKey(CourseInstance, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.course_instance}"

class StatusUpdate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='status_updates')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status by {self.user.username} at {self.timestamp}"

class CourseMaterial(models.Model):
    course_instance = models.ForeignKey(CourseInstance, on_delete=models.CASCADE, related_name='materials')
    file = models.FileField(upload_to='course_materials/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Material for {self.course_instance}"

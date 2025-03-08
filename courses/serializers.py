from rest_framework import serializers
from .models import Course, CourseInstance, Enrollment, Feedback, StatusUpdate, CourseMaterial

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description']

class CourseInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseInstance
        fields = ['id', 'course', 'semester', 'start_date', 'end_date', 'status', 'instructor']

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course_instance', 'enrolled_on']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'course_instance', 'user', 'text', 'rating', 'timestamp']

class StatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusUpdate
        fields = ['id', 'user', 'content', 'timestamp']

class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = ['id', 'course_instance', 'file', 'description', 'uploaded_at']

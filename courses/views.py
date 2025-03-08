from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from .models import Course, CourseInstance, Enrollment, Feedback, StatusUpdate, CourseMaterial
from .serializers import (
    CourseSerializer, CourseInstanceSerializer, EnrollmentSerializer,
    FeedbackSerializer, StatusUpdateSerializer, CourseMaterialSerializer
)
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not (self.request.user.role == 'teacher' or self.request.user.is_superuser):
            raise PermissionDenied("Only instructors can create courses.")
        serializer.save()

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class EnrollmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, instance_id, format=None):
        instance = get_object_or_404(CourseInstance, id=instance_id)
        if instance.status != 'Upcoming':
            return Response({"detail": "Enrollment allowed only for upcoming course instances."},
                            status=status.HTTP_400_BAD_REQUEST)
        if instance.enrollments.count() >= 30:
            return Response({"detail": "This course instance is full."},
                            status=status.HTTP_400_BAD_REQUEST)
        student_enrollments = Enrollment.objects.filter(student=request.user, course_instance__semester=instance.semester).count()
        if student_enrollments >= 5:
            return Response({"detail": "You are already enrolled in 5 courses this semester."},
                            status=status.HTTP_400_BAD_REQUEST)
        enrollment = Enrollment.objects.create(student=request.user, course_instance=instance)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RemoveStudentView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request, instance_id, format=None):
        instance = get_object_or_404(CourseInstance, id=instance_id)
        if instance.instructor != request.user:
            raise PermissionDenied("You are not the instructor for this course instance.")
        student_id = request.data.get('student_id')
        if not student_id:
            return Response({"detail": "student_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        enrollment = Enrollment.objects.filter(course_instance=instance, student__id=student_id).first()
        if not enrollment:
            return Response({"detail": "Student not enrolled."}, status=status.HTTP_400_BAD_REQUEST)
        enrollment.delete()
        return Response({"detail": "Student removed successfully."}, status=status.HTTP_200_OK)

class FeedbackListCreateView(generics.ListCreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        instance_id = self.kwargs.get('pk')
        return Feedback.objects.filter(course_instance__id=instance_id)

    def perform_create(self, serializer):
        instance_id = self.kwargs.get('pk')
        instance = get_object_or_404(CourseInstance, id=instance_id)
        serializer.save(course_instance=instance, user=self.request.user)

class StatusUpdateCreateView(generics.CreateAPIView):
    queryset = StatusUpdate.objects.all()
    serializer_class = StatusUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StatusUpdateListView(generics.ListAPIView):
    serializer_class = StatusUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs.get('username')
        return StatusUpdate.objects.filter(user__username=username)

class CourseMaterialListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseMaterialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        instance_id = self.kwargs.get('pk')
        return CourseMaterial.objects.filter(course_instance__id=instance_id)

    def perform_create(self, serializer):
        instance_id = self.kwargs.get('pk')
        instance = get_object_or_404(CourseInstance, id=instance_id)
        if self.request.user != instance.instructor:
            raise PermissionDenied("Only the course instructor can upload materials.")
        serializer.save(course_instance=instance)

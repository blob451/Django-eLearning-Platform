from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Course, Enrollment, Feedback, StatusUpdate, CourseMaterial
from .serializers import (
    CourseSerializer, EnrollmentSerializer, FeedbackSerializer,
    StatusUpdateSerializer, CourseMaterialSerializer
)
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher

# List all courses and allow teachers to create courses
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'teacher':
            raise PermissionDenied("Only teachers can create courses.")
        serializer.save(teacher=self.request.user)

# Retrieve, update, or delete a course
class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

# Enrollment endpoint: student enrolls in a course
class EnrollCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        if request.user.role != 'student':
            raise PermissionDenied("Only students can enroll.")
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course,
            defaults={'is_active': True}
        )
        if not created:
            return Response({"detail": "Already enrolled."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Remove student endpoint: teacher removes a student
class RemoveStudentView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        if course.teacher != request.user:
            raise PermissionDenied("You are not the teacher of this course.")
        student_id = request.data.get('student_id')
        if not student_id:
            return Response({"detail": "student_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        enrollment = Enrollment.objects.filter(course=course, student__id=student_id, is_active=True).first()
        if not enrollment:
            return Response({"detail": "Student not enrolled or already removed."}, status=status.HTTP_400_BAD_REQUEST)
        enrollment.is_active = False
        enrollment.save()
        return Response({"detail": "Student removed successfully."}, status=status.HTTP_200_OK)

# Feedback endpoint: list and create feedback for a course
class FeedbackListCreateView(generics.ListCreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('pk')
        return Feedback.objects.filter(course__id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs.get('pk')
        course = get_object_or_404(Course, pk=course_id)
        serializer.save(course=course, user=self.request.user)

# Status update endpoints
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

# Course materials endpoints
class CourseMaterialListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseMaterialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('pk')
        return CourseMaterial.objects.filter(course__id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs.get('pk')
        course = get_object_or_404(Course, pk=course_id)
        if self.request.user != course.teacher:
            raise PermissionDenied("Only the course teacher can upload materials.")
        serializer.save(course=course)

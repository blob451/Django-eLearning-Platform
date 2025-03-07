from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher
from .models import Course
from .serializers import CourseSerializer  # Assume you have created a serializer

class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacher]  # Only authenticated teachers can create courses

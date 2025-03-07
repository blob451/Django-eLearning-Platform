from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer, UserSerializer
from .models import User
from users.permissions import IsTeacher

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return User.objects.filter(username__icontains=query)

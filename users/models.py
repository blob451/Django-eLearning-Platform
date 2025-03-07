from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='student')

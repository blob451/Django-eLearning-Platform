from django.urls import path
from .views import (
    CourseListCreateView, CourseDetailView, EnrollCourseView, RemoveStudentView,
    FeedbackListCreateView, StatusUpdateCreateView, StatusUpdateListView,
    CourseMaterialListCreateView,
)

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:pk>/enroll/', EnrollCourseView.as_view(), name='course-enroll'),
    path('courses/<int:pk>/remove_student/', RemoveStudentView.as_view(), name='course-remove-student'),
    path('courses/<int:pk>/feedback/', FeedbackListCreateView.as_view(), name='course-feedback'),
    path('courses/<int:pk>/materials/', CourseMaterialListCreateView.as_view(), name='course-materials'),
    path('status_updates/', StatusUpdateCreateView.as_view(), name='status-update-create'),
    path('status_updates/<str:username>/', StatusUpdateListView.as_view(), name='status-update-list'),
]

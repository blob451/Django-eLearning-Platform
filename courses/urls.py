from django.urls import path
from .views import (
    CourseListView, CourseDetailView, CourseCreateView, CourseEditView, CourseDeleteView,
    enrollment_view, course_enrollment_manage_view
    # (Other views such as feedback can be added as needed)
)

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-catalog'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/create/', CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/edit/', CourseEditView.as_view(), name='course-edit'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),
    path('courses/enroll/<int:instance_id>/', enrollment_view, name='enroll_instance'),
    path('courses/<int:pk>/manage_enrollments/', course_enrollment_manage_view, name='course-enrollment-manage'),
]

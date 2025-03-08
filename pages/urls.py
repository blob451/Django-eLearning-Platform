from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('courses/', views.course_catalog_view, name='course_catalog'),
    path('courses/<int:pk>/', views.course_detail_view, name='course_detail'),
    path('courses/enroll/<int:instance_id>/', views.enroll_in_instance, name='enroll_instance'),
    path('chat/', views.chat_view, name='chat'),
]

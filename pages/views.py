from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from courses.models import Course, CourseInstance, Enrollment
from django.utils import timezone

def home_view(request):
    return render(request, 'home.html')

def profile_view(request):
    return render(request, 'profile.html')

def dashboard_view(request):
    enrollments = request.user.enrollments.all() if request.user.is_authenticated else None
    return render(request, 'dashboard.html', {'enrollments': enrollments})

def course_catalog_view(request):
    courses = Course.objects.all()
    return render(request, 'course_catalog.html', {'courses': courses})

def course_detail_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    instances = course.instances.all()
    return render(request, 'course_detail.html', {'course': course, 'instances': instances})

@login_required
def enroll_in_instance(request, instance_id):
    instance = get_object_or_404(CourseInstance, id=instance_id)
    if instance.status != 'Upcoming':
        messages.error(request, "Enrollment is allowed only for upcoming course instances.")
        return redirect('course_detail', pk=instance.course.id)
    if instance.enrollments.count() >= 30:
        messages.error(request, "This course instance is full.")
        return redirect('course_detail', pk=instance.course.id)
    count = request.user.enrollments.filter(course_instance__semester=instance.semester).count()
    if count >= 5:
        messages.error(request, "You are already enrolled in 5 courses this semester.")
        return redirect('dashboard')
    Enrollment.objects.create(student=request.user, course_instance=instance)
    messages.success(request, "You have been enrolled successfully!")
    return redirect('dashboard')

def chat_view(request):
    return render(request, 'chat.html')

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")
        from users.models import User
        user = User.objects.create_user(username=username, email=email, password=password, role=role)
        user.is_active = False  # Pending approval
        user.save()
        messages.success(request, "Account created. Await approval.")
        return redirect('login')
    return render(request, 'login.html')

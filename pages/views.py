from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from courses.models import Course, CourseInstance, Enrollment, Assignment
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

def home_view(request):
    return render(request, 'home.html')

def profile_view(request):
    # This view might be a generic dashboard; we now add a dedicated profile page below.
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

@login_required
def chat_view(request):
    return render(request, 'chat.html')

def signup_view(request):
    from users.forms import RegistrationForm
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Assign user to appropriate group
            from django.contrib.auth.models import Group
            role = form.cleaned_data.get("role").lower()
            if role == "teacher":
                group, _ = Group.objects.get_or_create(name="Teachers")
                group.user_set.add(user)
            else:
                group, _ = Group.objects.get_or_create(name="Students")
                group.user_set.add(user)
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()
    return render(request, "signup.html", {"form": form})

def custom_logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('home')

@login_required
def instructor_manage_view(request):
    if request.user.role != 'teacher' and not request.user.is_superuser:
        messages.error(request, "Only instructors can access the management page.")
        return redirect('home')
    instances = CourseInstance.objects.filter(instructor=request.user)
    return render(request, 'instructor_manage.html', {'instances': instances})

@login_required
def profile_detail_view(request, username):
    # Ensure that the profile can be viewed by the user themselves or publicly (depending on your privacy design)
    profile_user = get_object_or_404(User, username=username)
    # For a student, get enrolled courses; for a teacher, get courses taught.
    if profile_user.role.lower() == "teacher":
        # Query courses taught by this teacher (via course instances)
        courses_taught = profile_user.course_instances.select_related('course').all()
        course_list = {instance.course for instance in courses_taught}
    else:
        # For students, get enrollments
        enrollments = profile_user.enrollments.select_related('course_instance__course').all()
        course_list = [en.course_instance for en in enrollments]

    # Recent status updates (assuming StatusUpdate is defined in courses.models)
    status_updates = profile_user.status_updates.all().order_by('-timestamp')[:5]

    # Upcoming deadlines: for students, gather assignments from enrolled courses with due_date in the future
    upcoming_deadlines = None
    if profile_user.role.lower() != "teacher":
        today = timezone.now().date()
        # Use Assignment model defined in courses.models
        from courses.models import Assignment
        upcoming_deadlines = Assignment.objects.filter(
            course__enrollments__student=profile_user,
            due_date__gte=today
        ).order_by('due_date').distinct()[:5]

    context = {
        'profile_user': profile_user,
        'course_list': course_list,
        'status_updates': status_updates,
        'upcoming_deadlines': upcoming_deadlines,
    }
    return render(request, 'profile_detail.html', context)

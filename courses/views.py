from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Course, CourseInstance, Enrollment, Feedback, StatusUpdate, CourseMaterial
from .forms import CourseForm, CourseMaterialForm

# List view for course catalog
class CourseListView(ListView):
    model = Course
    template_name = 'course_catalog.html'
    context_object_name = 'courses'

# Detail view for a course
class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'

# Mixin to restrict access to teachers
class TeacherRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role.lower() == 'teacher' or self.request.user.is_superuser

# Course creation view for teachers
class CourseCreateView(TeacherRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_create.html'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('course-detail', kwargs={'pk': self.object.pk})

# Course editing view for teachers
class CourseEditView(TeacherRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_edit.html'
    
    def get_success_url(self):
        return reverse_lazy('course-detail', kwargs={'pk': self.object.pk})

# Course deletion view for teachers
class CourseDeleteView(TeacherRequiredMixin, DeleteView):
    model = Course
    template_name = 'course_delete.html'
    success_url = reverse_lazy('course-catalog')

# Enrollment view (function-based for simplicity)
def enrollment_view(request, instance_id):
    instance = get_object_or_404(CourseInstance, id=instance_id)
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to enroll.")
        return redirect('login')
    if instance.status != 'Upcoming':
        messages.error(request, "Enrollment is allowed only for upcoming course instances.")
        return redirect('course-detail', pk=instance.course.id)
    if instance.enrollments.count() >= 30:
        messages.error(request, "This course instance is full.")
        return redirect('course-detail', pk=instance.course.id)
    count = request.user.enrollments.filter(course_instance__semester=instance.semester).count()
    if count >= 5:
        messages.error(request, "You are already enrolled in 5 courses this semester.")
        return redirect('dashboard')
    Enrollment.objects.create(student=request.user, course_instance=instance)
    messages.success(request, "You have been enrolled successfully!")
    return redirect('dashboard')

# Enrollment management view for teachers
def course_enrollment_manage_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if not request.user.is_authenticated or (request.user.role.lower() != 'teacher' and not request.user.is_superuser):
        messages.error(request, "Only teachers can manage enrollments.")
        return redirect('course-detail', pk=course.pk)
    enrollments = Enrollment.objects.filter(course_instance__course=course)
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        if not student_id:
            messages.error(request, "Student ID is required.")
        else:
            enrollment = Enrollment.objects.filter(course_instance__course=course, student__id=student_id).first()
            if enrollment:
                enrollment.delete()
                messages.success(request, "Student removed successfully.")
            else:
                messages.error(request, "Enrollment not found.")
        return redirect('course-enrollment-manage', pk=course.pk)
    context = {
        'course': course,
        'enrollments': enrollments,
    }
    return render(request, 'course_enrollment_manage.html', context)

from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

def profile_view(request):
    return render(request, 'profile.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def login_view(request):
    return render(request, 'login.html')

def course_detail_view(request, pk):
    # In a real application, you would fetch course details from the database.
    context = {'course_id': pk}
    return render(request, 'course_detail.html', context)

def course_catalog_view(request):
    return render(request, 'course_catalog.html')

def chat_view(request):
    return render(request, 'chat.html')

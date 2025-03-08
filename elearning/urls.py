from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin

def home_view(request):
    return HttpResponse("<h1>Welcome to My eLearning Platform</h1>")

urlpatterns = [
    path('', home_view),  # Now http://127.0.0.1:8000/ won't 404
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/', include('courses.urls')),
    path('notifications/', include('notifications.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

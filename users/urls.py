from django.urls import path
from .views import UserRegistrationView, UserSearchView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('search/', UserSearchView.as_view(), name='user-search'),
]

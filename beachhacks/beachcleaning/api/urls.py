from django.urls import path
from .views import BeachesView, LoginView, LogoutView, RegisterView

urlpatterns = [
    path('beaches/', BeachesView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/register/', RegisterView.as_view())
]

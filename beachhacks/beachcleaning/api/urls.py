from django.urls import path
from .views import BeachesView

urlpatterns = [
    path('beaches/', BeachesView.as_view()),
]

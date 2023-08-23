from django.urls import path
from subjects.views import Subjects

urlpatterns = [
    path('', Subjects.as_view()),
]
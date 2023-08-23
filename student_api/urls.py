from django.urls import path
from student_api.views import Students, StudentDetail

urlpatterns = [
    path('', Students.as_view()),
    path('<str:pk>', StudentDetail.as_view())
]
from django.urls import path
from user.views import UserCustomAuth
from .viewsets import UserDetailAPI, RegisterUserAPIView

urlpatterns = [
    path('<str:pk>', UserCustomAuth.as_view()),
    path("get-details",UserDetailAPI.as_view()),
    path('register', RegisterUserAPIView.as_view()),
]
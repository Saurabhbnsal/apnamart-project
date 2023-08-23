from django.urls import path
from marks.views import Marks

urlpatterns = [
    path('', Marks.as_view()),
    # path('', Marks.as_view()),
    # path('<str:pk>', SubjectDetail.as_view())
]
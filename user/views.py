from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework import status, generics
from subjects.models import SubjectModel
from subjects.serializers import SubjectSerializer
import math
from datetime import datetime
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class UserCustomAuth(generics.GenericAPIView):
     def get(self, request, format=None):
        current_user = request.user
       
        content = {
            # 'user': current_user,
            'id': current_user.id,  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


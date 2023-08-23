from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework import status, generics
from marks.models import MarksModel
from marks.serializers import MarkSerializer
import math
from datetime import datetime
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from subjects.models import SubjectModel
from django.contrib.auth.models import User
from django.db.models import Max
from django.conf import settings
from django.core.cache import cache

class Marks(generics.GenericAPIView):
    serializer_class = MarkSerializer
    queryset = MarksModel.objects.all()
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"marks": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
    def highest_marks_overall(self):
        cache_key = 'highest_marks_overall'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        highest_marks_overall =  MarksModel.objects.all().aggregate(max_marks=Max('marks'))['max_marks']
        highest_score_object = MarksModel.objects.filter(marks=highest_marks_overall)[:1].values('user_id', 'subject_id')[0]
        highest_scorer_user_id = highest_score_object['user_id']
        highest_scored_subject_name = SubjectModel.objects.values('name').get(id=highest_score_object['subject_id'])['name']
        highest_overall_user = User.objects.values('username').get(id=highest_scorer_user_id)
        results =  {
            "marks": highest_marks_overall,
            "user_name": highest_overall_user['username'],
            "subject": highest_scored_subject_name,
            }
        cache.set(cache_key, results, 3600)
        return results

    def highest_marks_in_subject(self, user_id, subject_id):
        cache_key = 'highest_marks_in_subject_' + subject_id
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data
        
        max_marks = MarksModel.objects.filter(subject_id=subject_id).aggregate(max_marks=Max('marks'))['max_marks']
        highest_score_object = MarksModel.objects.filter(marks=max_marks)[:1].values('user_id')[0]
        highest_scorer_user_id = highest_score_object['user_id']
        highest_score_user = User.objects.values('username').get(id=highest_scorer_user_id)

        data = {
            "marks": max_marks,
            "user_name": highest_score_user['username'],
        }
        cache.set(cache_key, data, 3600)
        return data
   
    def get(self, request):
        user_id = request.user.id
        highest_score_object = self.highest_marks_overall()
        
        if 'subject_id' in request.data:
           subject_id = request.data['subject_id']
           highest_score_in_subject = self.highest_marks_in_subject(user_id, subject_id)
           self_marks = MarksModel.objects.values('marks').get(user_id=user_id, subject_id=subject_id)
        else:
           return Response({"status": "fail", "message": 'Need Subject Id'}, status=status.HTTP_400_BAD_REQUEST)
       
        return Response({
            "status": "success",
            "marks": self_marks['marks'],
            "highest_score_in_subject": highest_score_in_subject,
            "highest_score_overall": highest_score_object
          
        })

   




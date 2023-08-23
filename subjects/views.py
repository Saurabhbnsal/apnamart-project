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

class Subjects(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)

    serializer_class = SubjectSerializer
    queryset = SubjectModel.objects.all()

  
    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        subjects = SubjectModel.objects.all()
        total_subjects = subjects.count()
        if search_param:
            subjects = subjects.filter(name__icontains=search_param)
        serializer = self.serializer_class(subjects[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_subjects,
            "page": page_num,
            "last_page": math.ceil(total_subjects / limit_num),
            "subjects": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"subject": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


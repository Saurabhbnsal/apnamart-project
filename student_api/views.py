from rest_framework.response import Response
from rest_framework import status, generics
from student_api.models import StudentModel
from student_api.serializers import StudentSerializer
import math
from datetime import datetime

class Students(generics.GenericAPIView):
    serializer_class = StudentSerializer
    queryset = StudentModel.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        students = StudentModel.objects.all()
        total_students = students.count()
        if search_param:
            students = students.filter(name__icontains=search_param)
        serializer = self.serializer_class(students[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_students,
            "page": page_num,
            "last_page": math.ceil(total_students / limit_num),
            "students": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"student": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(generics.GenericAPIView):
    queryset = StudentModel.objects.all()
    serializer_class = StudentSerializer

    def get_student(self, pk):
        try:
            return StudentModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        student = self.get_student(pk=pk)
        if nstudent == None:
            return Response({"status": "fail", "message": f"student with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(student)
        return Response({"status": "success", "data": {"student": serializer.data}})

    def patch(self, request, pk):
        student = self.get_student(pk)
        if student == None:
            return Response({"status": "fail", "message": f"student with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['updatedAt'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "data": {"student": serializer.data}})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = self.get_student(pk)
        if student == None:
            return Response({"status": "fail", "message": f"student with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
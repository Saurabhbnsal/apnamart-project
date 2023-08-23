from rest_framework import serializers
from marks.models import MarksModel


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarksModel
        fields = '__all__'
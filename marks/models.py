import uuid
from django.db import models
from subjects.models import SubjectModel
from django.contrib.auth.models import User
# Create your models here.
class MarksModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    marks = models.IntegerField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectModel, null=True, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "marks"
        ordering = ['-createdAt']

        def __str__(self) -> str:
            return self.id
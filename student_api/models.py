import uuid
from django.db import models


class StudentModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "students"
        ordering = ['-createdAt']

        def __str__(self) -> str:
            return self.name
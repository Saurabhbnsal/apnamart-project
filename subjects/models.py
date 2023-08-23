import uuid
from django.db import models

# Create your models here.

class SubjectModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "subjects"
        ordering = ['-createdAt']

        def __str__(self) -> str:
            return self.name
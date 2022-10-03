from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class Content(models.Model):
    title = models.CharField(max_length=50)
    module = models.TextField()
    students = models.IntegerField()
    description = models.TextField(null=True)
    is_active = models.BooleanField(null=True, default=False)

    def __repr__(self):
        return f"<[{self.id}] {self.title} - {self.module}>"



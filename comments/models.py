from django.db import models
from files.models import *
from auth_user.models import *
import uuid

# Create your models here.

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()

    fk_user = models.ForeignKey(User, related_name='comment_responsible', on_delete=models.CASCADE)
    files = models.ManyToManyField(File, related_name='comment_files')
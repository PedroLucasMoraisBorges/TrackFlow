from django.db import models
from files.models import *
import uuid

# Create your models here.

class Stage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    dt_creation = models.DateField()

    files = models.ManyToManyField(File, related_name='stage_files')
    stages = models.ManyToManyField('self', related_name='substages', symmetrical=False)
    comments = models.ManyToManyField(File, related_name='stage_comments')

from django.db import models
from projects.models import *
from files.models import *
from comments.models import *
import uuid

# Create your models here.

class Milestone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    description = models.TextField(null=False)
    order = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    
    fk_project = models.ForeignKey(Project, related_name='project', on_delete=models.CASCADE)
    files = models.ManyToManyField(File, related_name='milestone_files')
    comments = models.ManyToManyField(File, related_name='milestone_comments')

    def __str__(self):
        return f"{self.fk_project.name} - {self.name}"
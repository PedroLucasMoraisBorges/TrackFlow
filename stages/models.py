from django.db import models
from files.models import *
import uuid
from milestones.models import Milestone

# Create your models here.

class Stage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    dt_creation = models.DateTimeField(auto_now_add=True)
    fk_milestone = models.ForeignKey(Milestone, related_name='milestone_stage', null=True, on_delete=models.CASCADE)
    files = models.ManyToManyField(File, related_name='stage_files')
    fk_stage = models.ForeignKey('self', related_name='substages', null=True, on_delete=models.CASCADE)
    comments = models.ManyToManyField(File, related_name='stage_comments')
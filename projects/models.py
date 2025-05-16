from django.db import models
from auth_user.models import *
import uuid

# Create your models here.
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    description = models.TextField(null=False)
    is_completed = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    dt_created = models.DateField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    fk_manager = models.ForeignKey(User, related_name='project_manager', on_delete=models.CASCADE)
    fk_owner = models.ForeignKey(User, related_name='project_owner', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
class Templates(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metadata = models.JSONField(default=dict, blank=True)
    fk_user = models.ForeignKey(User, related_name='template_manager', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Template - {self.fk_user.name}'

class Evaluation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fk_user = models.ForeignKey(User, related_name='writer', on_delete=models.CASCADE, null=True)
    fk_template = models.ForeignKey(Templates, related_name='fk_template', on_delete=models.CASCADE, null=True)
    rate = models.FloatField(default=0)
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
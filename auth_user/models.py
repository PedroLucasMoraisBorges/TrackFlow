from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid
# Create your models here.
types = [
    ('G', 'Gestor'),
    ('U', 'User')
]

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    name = models.CharField(max_length = 256)
    email = models.EmailField(unique = True, blank = False)
    type = models.CharField(choices=types, blank=False, max_length=1)
    clients = models.ManyToManyField('self', related_name='managed_by', symmetrical=False, null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permissions',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name
    
    @property
    def user_image(self):
        if " " in self.name:
           name = self.name.split(" ")
        else: name = self.name

        firstName = name[0]
        secondName = name[1]
        
        return firstName[0].upper() + secondName[0].upper()
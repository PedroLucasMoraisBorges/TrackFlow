from django import template
from django.db.models import Q, F
from .models import *
from .forms import *

register = template.Library()

@register.simple_tag
def get_projects(user):
    my_projects = Project.objects.filter(fk_manager=user)
    return my_projects
from django import template
from django.db.models import Q
from .models import Project

register = template.Library()

@register.simple_tag
def get_projects(user):
    my_projects = Project.objects.filter(Q(fk_manager=user) | Q(fk_owner=user))
    return my_projects

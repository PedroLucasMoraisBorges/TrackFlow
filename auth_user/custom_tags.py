from django import template
from django.db.models import Q, F
from .models import *
from .forms import *

register = template.Library()

@register.simple_tag
def get_clients(user):
    my_clients = user.clients.all()
    return my_clients
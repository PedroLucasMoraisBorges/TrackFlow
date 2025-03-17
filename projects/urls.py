from django.urls import path
from .views import *

urlpatterns = [
    path('viewProject/<str:id>', ViewProject.as_view(), name='view_project')
]
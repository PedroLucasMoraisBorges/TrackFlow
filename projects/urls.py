from django.urls import path
from .views import *

urlpatterns = [
    path('viewProject/<str:id>', ViewProject.as_view(), name='view_project'),
    path('myProjects/', Projects.as_view(), name='my_projects'),
    path('createProjectWithAi/', CreateProjectWithAi.as_view(), name='generate_project')
]
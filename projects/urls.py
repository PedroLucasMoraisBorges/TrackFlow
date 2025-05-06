from django.urls import path
from .views import *

urlpatterns = [
    path('viewProject/<str:id>', ViewProject.as_view(), name='view_project'),
    path('myProjects/', Projects.as_view(), name='my_projects'),
    path('createProjectWithAi/', CreateProjectWithAi.as_view(), name='generate_project'),
    path('aiPage/', AiPage.as_view(), name='ai_page'),
    path('deleteProject/<str:id>', DeleteProject.as_view(), name='delete_project'),
    path('copyProject/<str:id>', CopyProject.as_view(), name='copy_project'),
    path('completeProjects/', CompleteProjects.as_view(), name='complete_projects')
]
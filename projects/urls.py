from django.urls import path
from .views import *

urlpatterns = [
    path('viewProject/<str:id>', ViewProject.as_view(), name='view_project'),
    path('myProjects/', Projects.as_view(), name='my_projects'),
    path('createProjectWithAi/', CreateProjectWithAi.as_view(), name='generate_project'),
    path('aiPage/', AiPage.as_view(), name='ai_page'),
    path('deleteProject/<str:id>', DeleteProject.as_view(), name='delete_project'),
    path('copyProject/<str:id>', CopyProject.as_view(), name='copy_project'),
    path('completeProjects/', CompleteProjects.as_view(), name='complete_projects'),
    path('parseProjectToTemplate/<str:id>', CopyProjectToTemplate.as_view(), name='parse_project_to_template'),
    path('myTemplates/', MyTemplates.as_view(), name='my_templates'),
    path('rateTemplate/<str:id>', RateTemplate.as_view(), name='rate_template'),
    path('createProjectWithTemplate/<str:id>', CreateProjectWithTemplate.as_view(), name='create_project_with_template'),
    path('clientProjects/', ClientProjects.as_view(), name='client_projects')
]
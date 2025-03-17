from django.urls import path
from .views import *

urlpatterns = [
    path('project/<str:project_id>/registerMilestone/<str:milestone_id>/', RegisterMilestonePage.as_view(), name='register_milestone'),

    # API
    path('createMilestone/<str:id>', CreateMilestone.as_view(), name='create_milestone')
]
from django.urls import path
from .views import *

urlpatterns = [
    path('project/<str:project_id>/registerMilestone/<str:milestone_id>/', RegisterMilestonePage.as_view(), name='register_milestone'),
    path('finalizeMilestone/<str:id>', FinalizeMilestone.as_view(), name='finalize_milestone'),
    path('markLastMilestone/<str:id>', MarkLastMilestone.as_view(), name='mark_last_milestone'),
    path('deleteMilestone/<str:id>', DeleteMilestone.as_view(), name='delete_milestone'),

    # API
    path('createMilestone/<str:id>', CreateMilestone.as_view(), name='create_milestone')
]
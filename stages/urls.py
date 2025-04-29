from django.urls import path
from .views import *

urlpatterns = [
    path('createStage/<str:id>', CreateStage.as_view(), name='create_state'),
    path('editStage/<str:id>', EditStage.as_view(), name='edit_stage'),
    path('deleteStage/<str:id>', DeleteStage.as_view(), name='delete_stage')
]
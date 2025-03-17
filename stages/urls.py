from django.urls import path
from .views import *

urlpatterns = [
    path('createStage/<str:id>', CreateStage.as_view(), name='create_state')
]
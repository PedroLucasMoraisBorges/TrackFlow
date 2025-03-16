from django.urls import path
from .views import *

urlpatterns = [
    path('createStage/<str:id>/<str:type>', CreateStage.as_view(), name='create_state')
]
from django.urls import path
from .views import *

urlpatterns = [
    path('createFile/<str:id>/<str:type>', CreateFile.as_view(), name='create_file')
]
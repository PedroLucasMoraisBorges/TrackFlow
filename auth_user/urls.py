from django.urls import path
from .views import *

urlpatterns = [
    path('', Redirect.as_view(), name='redirect'),
    path('home', Home.as_view(), name='home'),
    path('login', Login.as_view(), name='login'),
    path('cadastro', Register.as_view(), name='register'),
    path('manager/clients', Clients.as_view(), name='clients'),
    path('clientPage/<str:id>', ClientPage.as_view(), name='client_page'),
    path('perfil', ProfileView.as_view(), name='profile'),
    path('templates', TemplatesView.as_view(), name='templates')
]
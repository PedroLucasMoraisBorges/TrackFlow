from django.urls import path
from .views import *

urlpatterns = [
    path('', Redirect.as_view(), name='redirect'),
    path('landingPage', LandingPage.as_view(), name='landing_page'),
    path('login', Login.as_view(), name='login'),
    path('cadastro', Register.as_view(), name='register'),
    path('manager/clients', Clients.as_view(), name='clients'),
    path('clientPage/<str:id>', ClientPage.as_view(), name='client_page')
]
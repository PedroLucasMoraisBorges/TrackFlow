from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View
from .forms import *
from .models import *

from projects.models import*
from projects.forms import *
from geralUtilits import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class LandingPage(View):
    def get(self, request):
        return render(request, 'landing_page.html')
    
# Classe para redirecionamento de tipo de usuário
class Redirect(View):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect('landing_page')
        if user.type == 'U':
            return redirect('client page')
        elif user.type == 'G':
            return redirect('clients')

# Logind de usuário geral
class Login(View):
    def get(self, request):
        form = AuthenticationForm()

        context = {
            'form' : form
        }

        return render(request, 'auth/login.html', context)

    def post(self, request):
        form = AuthenticationForm(request.POST)
        errors = getErrors([form])

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)

            # send_account_activation(user)
            # return redirect('alert_user_inactive')
            return redirect('')
        
        context = {
            'errors' : errors,
            'form'   : form
        }

        return render(request, 'auth/login.html', context)

# Cadastro de manager
class Register(View):
    def get(self, request):
        form = CustomUserCreationForm()

        context = {
            'form' : form
        }

        return render(request, 'auth/register.html', context)
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        errors = getErrors([form])

        if form.is_valid():
            user = form.save(commit=False)
            user.type = 'G'
            user.save()

            login(request, user)
            return redirect('/')
        
        context = {
            'form'   : form,
            'errors' : errors
        }

        return render(request, 'auth/register.html', context)

# Lista dos clientes cadastrados pelo manager
class Clients(View):
    def get(self, request):
        form = CustomUserCreationForm(request.POST)
        clients = request.user.clients.all()

        context = {
            'clients' : clients,
            'form'    : form
        }

        return render(request, 'manager/clients.html', context)
    
    def post(self, request):
        user = request.user
        form = CustomUserCreationForm(request.POST)
        clients = user.clients.all()

        errors = getErrors([form])

        if form.is_valid():
            client = form.save(commit=False)
            client.type = 'U'
            client.save()

            user.clients.add(client)
            user.save()

            return redirect('/')
        
        context = {
            'clients' :  clients,
            'form'    :  form,
            'errors'  :  errors
        }

        return render(request, 'manager/clients.html', context)
    
# Página de detalhes do cliente, servindo para manager e cliente com verificações no front-end
class ClientPage(View):
    def get(self, request, id):
        user = request.user
        client = User.objects.get(id)
        projects = Project.objects.filter(fl_owner = client, fk_manager = user)
        form = RegisterUserProjectForm()

        context = {
            'client' : client,
            'projects' : projects,
            'form' : form
        }

        return render(request, 'clientPage.html', context)
    
    def post(self, request, id):
        user = request.user
        client = User.objects.get(id)
        projects = Project.objects.filter(fl_owner = client, fk_manager = user)
        form = RegisterUserProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.fk_owner = client
            project.fk_manager = user
            project.save()

            return redirect('register milestone', id=project.id)

        context = {
            'client' : client,
            'projects' : projects,
            'form' : form,
            'errors' : getErrors([form])
        }

        return render(request, 'clientPage.html', context)
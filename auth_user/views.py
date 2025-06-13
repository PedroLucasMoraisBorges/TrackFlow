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

class Home(View):
    def get(self, request):
        projects = Project.objects.filter(fk_manager=request.user)
        user = User.objects.get(id=request.user.id)

        clients = user.clients.all()

        context = {
            'projects' : projects,
            'clients' : clients
        }
        return render(request, 'home.html', context)
    
# Classe para redirecionamento de tipo de usuário
class Redirect(View):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect('login')
        if user.type == 'U':
            return redirect('client_projects')
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
        form = AuthenticationForm(request, data=request.POST)
        errors = getErrors([form])
        
        if form.is_valid():
            user = form.get_user()  
            login(request, user)
            return redirect('/')
        
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
        print(errors)

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

        search = request.GET.get('search', "")

        clients = request.user.clients.filter(name__startswith=search)

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

        print(errors)

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
        client = User.objects.get(id=id)
        projects = Project.objects.filter(fk_owner = client, fk_manager = user)
        form = RegisterUserProjectForm()

        context = {
            'client' : client,
            'projects' : projects,
            'form' : form
        }

        return render(request, 'clientPage.html', context)
    
    def post(self, request, id):
        user = request.user
        client = User.objects.get(id=id)
        projects = Project.objects.filter(fk_owner = client, fk_manager = user)
        form = RegisterUserProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.fk_owner = client
            project.fk_manager = user
            project.save()

            return redirect('register_milestone', project_id=project.id, milestone_id='first_creation')

        context = {
            'client' : client,
            'projects' : projects,
            'form' : form,
            'errors' : getErrors([form])
        }

        return render(request, 'clientPage.html', context)
    
# Página de perfil do usuário
class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user = User.objects.get(id=request.user.id)
        projects = Project.objects.filter(fk_manager=user)
        clients = user.clients.all()

        context = {
            'user': user,
            'projects' : projects,
            'projects_count' : projects.count(),
            'clients' : clients,
            'clients_count' : clients.count()
        }

        return render(request, 'auth/profile.html', context)
    
from projects.forms import RateTemplateForm
# Página de templates do usuário
class TemplatesView(View):
    def get(self, request):
        form = RateTemplateForm()
        templates = Templates.objects.filter()

        templatesReturn = []

        for template in templates:
            rate = 0
            count_rates = 0

            evaluates = Evaluation.objects.filter(fk_template=template)

            for evaluate in evaluates:
                rate += evaluate.rate
                count_rates += 1
        
            templatesReturn.append(
                {
                    'info' : template,
                    'rate' : round(rate/count_rates, 1) if count_rates >= 1 else "Sem avaliações",
                    'rate_count' : count_rates
                }
            )


        context = {
            'templates': templatesReturn,
            'form' : form
        }

        return render(request, 'manager/templates.html', context)
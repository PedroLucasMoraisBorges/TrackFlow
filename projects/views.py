from django.shortcuts import render
from django.views import View
from .models import *
from .forms  import  * 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from geralUtilits import *

# Create your views here.
class Projects(View):
    def get(self, request):
        user = request.user
        projects = Project.objects.filter(fk_manager = user)
        form = RegisterProjectForm(user=request.user)

        context = {
            'projects' : projects,
            'form'     : form
        }

        return render(request, 'manager/projects.html', context)
    
class RegisterProject(APIView):
    def post(self, request):
        user = request.user
        form = RegisterProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.fk_manager = user
            project.save()

            return Response(
                {
                    'message': 'Projeto Cadastrado',
                    'project' : {
                        'id' : project.id,
                        'name' : project.name,
                    }
                }, status=status.HTTP_201_CREATED
            )
        
        errors = getErrors([form])

        return Response(
            {
                'message' : 'Erro no Formulário',
                'errors' : errors
            }, status= status.HTTP_400_BAD_REQUEST
        )
from django.shortcuts import render
from django.views import View
from .models import *
from .forms  import  * 
from milestones.models import *
from milestones.forms import *
from stages.models import *
from stages.forms import *
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

        return Response(
            {
                'message' : 'Erro no Formulário',
                'errors' : getErrors([form])
            }, status= status.HTTP_400_BAD_REQUEST
        )
    
class ViewProject(View):
    def get(self, request, id):
        project = Project.objects.get(id=id)
        edit_project_form = EditProjectForm(instance=project)

        project_milestones = Milestone.objects.filter(fk_project = project)
        returning_milestones = []

        for mls in project_milestones:
            stages = mls.stages.order_by('dt_creation')
            returning_stages = []
            files = mls.files.all()

            for stg in stages:
                stg_files = stg.files.all()
                stg_stgs = stg.stages.all()
                sub_stages = []
                
                for sub_stage in stg_stgs:
                    sub_stages.append(
                        {
                            'info' : sub_stage,
                            'form' : EditStageForm(instance=sub_stage)
                        }
                    )

                form = EditStageForm(instance=stg)

                returning_stages.append(
                    {   
                        'info' : stg,
                        'files' : stg_files,
                        'sub_stages' : sub_stages,
                        'form' : form
                    }
                )

            returning_milestones.append(
                {
                'info' : mls,
                'files' : files,
                'stages' : returning_stages,
                'form' : EditMilestoneForm(instance=mls)
                }
            )
        
        context = {
            'projetc' : project,
            'edit_project_form' : edit_project_form,
            'milestones' : returning_milestones
        }

        return render(request, 'manager/viewProject.html', context)
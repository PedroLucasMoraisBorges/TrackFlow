from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms  import  *
from milestones.forms import * 
from milestones.models import *
from files.forms import *
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
    
    def post(self, request):
        user = request.user
        form = RegisterProjectForm(request.POST, user=user)
        projects = Project.objects.filter(fk_manager = user)

        print(form.errors)
        if form.is_valid():
            project = form.save(commit=False)
            project.fk_manager = user
            project.save()

            return redirect('register_milestone', project_id=project.id, milestone_id='first_creation')

        context = {
            'projects' : projects,
            'form'     : form,
            'errors'   : getErrors([form])
        }

        return render(request, 'manager/projects.html', context)
    
class ViewProject(View):
    def get(self, request, id):
        project = Project.objects.get(id=id)
        edit_project_form = EditProjectForm(instance=project)

        project_milestones = Milestone.objects.filter(fk_project = project)
        returning_milestones = []

        for mls in project_milestones:
            stages = mls.stages.order_by('dt_creation')
            files = mls.files.all()

            returning_milestones.append(
                {
                    'info' : mls,
                    'files' : files,
                    'stages' : stages
                }
            )
        
        context = {
            'projetc' : project,
            'edit_project_form' : edit_project_form,
            'milestones' : returning_milestones,
            'file_form' : RegisterFileForm(),
        }

        return render(request, 'manager/viewProject.html', context)
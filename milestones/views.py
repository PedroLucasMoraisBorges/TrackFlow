from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import *
from .models import *
from stages.models import *
from stages.forms import *
from files.forms import *
from files.models import *
from projects.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class RegisterMilestonePage(View):
    def get(self, request, project_id, milestone_id=None):
        project = get_object_or_404(Project, id=project_id)

        milestone = None
        stage_list = []
        files = []
        images = []

        if milestone_id != 'first_creation':
            milestone = get_object_or_404(Milestone, id=milestone_id)
            stages = milestone.stages.all()

            for stage in stages:
                stage_list.append(
                    {
                        'id' : stage.id,
                        'name' : stage.name,
                        'description' : stage.description,
                        'files' : stage.files.all()
                    }
                )
            files = milestone.files.all()

        context = {
            'project' : project,
            'milestone' : milestone,
            'milestoneForm' : RegisterMilestoneForm(),
            'stageForm' : RegisterStageForm(),
            'stages' : stage_list,
            'file_form' : RegisterFileForm(),
            'files' : files,
        }

        return render(request, 'manager/registerMilestone.html', context)

    def post(self, request, project_id, milestone_id=None):
        form = RegisterMilestoneForm(request.POST)
        project = get_object_or_404(Project, id=project_id)

        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.fk_project = project
            milestone.save()

            return redirect('register_milestone', project_id=project_id, milestone_id=milestone.id)

class CreateMilestone(APIView):
    def post(self, request, id):
        project = get_object_or_404(Project, id=id)
        form = RegisterMilestoneForm(request.POST)


        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.fk_project = project
            milestone.save()

            return Response(
                {
                    "message": "Marco criado com sucesso",
                    "milestone": {
                        "id": milestone.id,
                        "name": milestone.name,
                        "description": milestone.description,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response({"error": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST)

class FinalizeMilestone(View):
    def get(self, request, id):
        milestone = Milestone.objects.get(id=id)
        milestone_historic = Milestone.objects.filter(fk_project=milestone.fk_project).order_by("order")

        milestone.order = milestone_historic.last().order + 1
        milestone.save()

        return redirect('register_milestone', project_id=milestone.fk_project.id, milestone_id='first_creation')
    
class MarkLastMilestone(View):
    def get(self, request, id):
        milestone = Milestone.objects.get(id=id)
        milestone_historic = Milestone.objects.filter(fk_project=milestone.fk_project).order_by("order")

        milestone.order = milestone_historic.last().order + 1
        milestone.save()

        project = Project.objects.get(id=milestone.fk_project.id)

        return redirect('view_project', id=project.id)
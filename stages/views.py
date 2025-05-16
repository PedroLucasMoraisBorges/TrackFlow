from django.shortcuts import render
from .models import *
from .forms import *
from milestones.models import *
from geralUtilits import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class CreateStage(APIView):
    def post(self, request, id):
        form = RegisterStageForm(request.POST, request.FILES)
        milestone = Milestone.objects.get(id=id)

        project = milestone.fk_project
        milestones_object = project.metadata.get("milestones", [])

        if form.is_valid():
            stage = form.save(commit=False)
            stage.fk_milestone = milestone
            stage.save()

            for milestone_object in milestones_object:
                
                if milestone_object["id"] == str(milestone.id):
                    milestone_object["milestone_stages"].append({
                        "id": str(stage.id),
                        'stage_name': stage.name,
                        'description': stage.description
                    })
                    break
            
            project.metadata["milestones"] = milestones_object
            project.save()

            return Response(
                {   
                    'message' : 'Etapa cadastrada com sucesso!',
                    'stage' : {
                        'id' : stage.id,
                        'name' : stage.name,
                        'stage_description' : stage.description
                    }
                }, status = status.HTTP_201_CREATED
            )
        
        return Response(
            {
                'message' : 'Erro no formulário',
                'errors' : getErrors([form])
            }, status=status.HTTP_404_NOT_FOUND
        )
    
class EditStage(APIView):
    def put(self, request, id):
        stage = Stage.objects.get(id=id)
        form = EditStageForm(request.POST, request.FILES, instance=stage)


        if form.is_valid():
            stage = form.save()

            return Response(
                {   
                    'message' : 'Etapa editada com sucesso!',
                    'stage' : {
                        'id' : stage.id,
                        'name' : stage.name,
                        'description' : stage.description
                    }
                }, status = status.HTTP_201_CREATED
            )

        return Response(
            {
                'message' : 'Falha no formulário',
                'errors' : getErrors([form])
            }, status = status.HTTP_400_BAD_REQUEST
        )

class DeleteStage(APIView):
    def get(self, request, id):
        Stage.objects.delete(id=id)

        return Response(
            {   
                'message' : 'Etapa deletada com sucesso!',
            }, status = status.HTTP_200_OK
        )
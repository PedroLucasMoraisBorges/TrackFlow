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
    def post(self, request, id, type):
        form = RegisterStageForm(request.POST, request.FILES)
        milestone = Milestone.objects.get(id=id)

        if form.is_valid():
            stage = form.save()
            milestone.stages.add(stage)

            return Response(
                {   
                    'message' : 'Etapa cadastrada com sucesso!',
                    'stage' : {
                        'id' : stage.id,
                        'name' : stage.name,
                        'description' : stage.description
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
from django.shortcuts import render
from .models import *
from .forms import *
from django.views import View
from milestones.models import *
from stages.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class CreateFile(APIView):
    def post(self, request, id, type):
        form = RegisterFileForm(request.POST, request.FILES)

        target_object = None
        if type == 'milestone':
            target_object = Milestone.objects.get(id=id)
        if type == 'stage':
            target_object = Stage.objects.get(id=id)
    

        if form.is_valid():
            

            uploaded_file = request.FILES['file']
            file_type = uploaded_file.content_type  # Obtém o tipo MIME do arquivo

            # Mapeamento dos tipos MIME para categorias
            categories = {
                'image': ['image/jpeg', 'image/png', 'image/gif', 'image/bmp'],
                'pdf': ['application/pdf'],
                'word': ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
                'excel': ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
            }

            # Função para categorizar o tipo de arquivo
            file_category = None
            for category, mime_types in categories.items():
                if file_type in mime_types:
                    file_category = category
                    break

            # Se não encontrar uma categoria, retorna erro
            if not file_category:
                return Response(
                    {'error': 'Tipo de arquivo inválido.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            file = form.save(commit=False)
            file.type = file_category
            file.save()
            target_object.files.add(file)

            print(file_category)

            return Response(
                {
                    'message' : 'Upload concluído',
                    'file' : {
                        'id' : id,
                        'file_id' : file.id,
                        'url' : file.file.url,
                        'type' : file.type
                    },
                }, status=status.HTTP_201_CREATED
            )
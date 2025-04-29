from django.shortcuts import render, redirect
from django.urls import reverse
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
            stages = Stage.objects.filter(fk_milestone=mls).order_by('dt_creation')
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
    
from google import generativeai as genai
import json

class AiPage(View):
    def get(self, request):
        form = CreateProjectWithAiForm(manager=request.user)

        context = {
            'form' : form
        }

        return render(request, 'manager/aiPage.html', context)

class CreateProjectWithAi(APIView):
    def post(self, request):
        genai.configure(api_key="AIzaSyBE28Htrlf6l8Bdo41GV5SmQsxYSP46aPQ")
        model = genai.GenerativeModel('gemini-1.5-pro')

        prompt = request.data.get("description")  
        ownerId = request.data.get("owner")


        if not prompt:
            return Response({"error": "Descrição do projeto está vazia."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        complete_prompt = f"""
Você é uma IA especialista em gestão de projetos, com foco em estruturação estratégica de qualquer tipo de iniciativa — seja ela criativa, técnica, operacional ou pessoal. Sua função é transformar uma descrição detalhada de um projeto em uma estrutura hierárquica organizada com base em marcos (milestones) e etapas (stages), independentemente do setor ou natureza do projeto.

Regras gerais:
     1. Leia com atenção toda a descrição do projeto fornecida pelo usuário.
     2. Identifique os principais objetivos, entregas esperadas e atividades-chave descritas.
     3. Divida o projeto em marcos principais, representando fases, temas ou grandes entregas.
     4. Dentro de cada marco, defina etapas específicas, que são ações ou componentes detalhados daquela entrega.
     5. Utilize linguagem objetiva, técnica e adaptada ao contexto do projeto — seja ele corporativo, pessoal, artístico ou operacional.
     6. Nunca utilize nomes genéricos como “Etapa 1” ou “Marco 1”. Sempre nomeie com base no conteúdo específico.
     7. A saída deve ser exclusivamente no formato JSON, conforme a estrutura a seguir.
     8. A saída deve ser exclusivamente no formato JSON, obedecendo à estrutura abaixo.
     9. Não adicione a palavra json para identificar o objeto, isso atrapalha a manipulação dos dados.

Descrição do projeto fornecida pelo usuário:
{prompt}

Estrutura JSON obrigatória de saída:
{{
  "project_name": "Título inferido com base na descrição",
  "project_description": "Resumo conciso e técnico do projeto como um todo",
  "milestones": [
    {{
      "milestone_name": "Nome do marco (claro e descritivo)",
      "milestone_description": "Descrição do marco explicando sua função no projeto",
      "milestone_stages": [
        {{
          "stage_name": "Nome da etapa (específico e técnico)",
          "stage_description": "Descrição detalhada da etapa"
        }}
        // ... outras etapas
      ]
    }}
    // ... outros marcos
  ]
}}
"""
        response = model.generate_content(complete_prompt)
        
        project_data = json.loads(response.text)

        owner = User.objects.get(id=ownerId)

        

        project = Project.objects.create(
            name = project_data['project_name'],
            description = project_data['project_description'],
            fk_manager = request.user,
            fk_owner = owner
        )
        project.save()

        order = 0

        for mlst in project_data['milestones']:
            order += 1
            milestone = Milestone.objects.create(
                name = mlst['milestone_name'],
                description = mlst['milestone_description'],
                order = order,
                fk_project = project
            )
            milestone.save()

            for stage in mlst['milestone_stages']:
                stage = Stage.objects.create(
                    name = stage['stage_name'],
                    description = stage['stage_description'],
                    fk_milestone=milestone
                )
                stage.save()
        
        return Response({'redirect_url': reverse('view_project', kwargs={'id': project.id})}, status=201)

class DeleteProject(APIView):
    def get(self, request, id):
        Project.objects.delete(id=id)

        return Response(
            {   
                'message' : 'Projeto deletadu com sucesso!',
            }, status = status.HTTP_200_OK
        )

def createProjectWithObject(project_data, user):
    project = Project.objects.create(
            name = project_data['project_name'],
            description = project_data['project_description'],
            fk_manager = user,
        )
    project.save()

    order = 0

    for mlst in project_data['milestones']:
        order += 1
        milestone = Milestone.objects.create(
            name = mlst['milestone_name'],
            description = mlst['milestone_description'],
            order = order,
            fk_project = project
        )
        milestone.save()

        for stage in mlst['milestone_stages']:
            stage = Stage.objects.create(
                name = stage['stage_name'],
                description = stage['stage_description'],
                fk_milestone = milestone
            )
            stage.save()
    
    return project


class CopyProject(APIView):
    def get(self, request, id):
        project = Project.objects.get(id=id)

        object = {}
        milestone_list_objects = []

        object.update({
            "project_name": project.name,
            "project_description": project.description,
        })

        milestones = Milestone.objects.filter(fk_project=project).order_by('order')
        for mls in milestones:
            milestone_object = {
                "milestone_name": mls.name,
                "milestone_description": mls.description,
                "milestone_stages": []
            }
            stages = Stage.objects.filter(fk_milestone=mls).order_by('dt_creation')

            for stage in stages:
                milestone_object['milestone_stages'].append({
                    "stage_name": stage.name,
                    "stage_description": stage.description
                })
            
            milestone_list_objects.append(milestone_object)
        
        object.update({
            'milestones' : milestone_list_objects
        })

        jsonObject = json.dumps(object, indent=4, ensure_ascii=False)

        project = createProjectWithObject(object, request.user)
        return Response({'redirect_url': reverse('view_project', kwargs={'id': project.id})}, status=201)
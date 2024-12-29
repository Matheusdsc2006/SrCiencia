from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from srciencia_core.models.Turma import Turma, TurmaAluno
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

@login_required
def listar_alunos_turma(request, turma_id):
    try:
        # Filtrar os alunos visíveis inscritos na turma
        alunos_visiveis = TurmaAluno.objects.filter(
            turma_id=turma_id, visivel=True
        ).select_related('aluno')
        
        # Preparar os dados dos alunos
        alunos_data = [
            {
                "nome": aluno.aluno.get_full_name() or aluno.aluno.username,  # Nome completo ou username
                "email": aluno.aluno.email  # Email do aluno
            }
            for aluno in alunos_visiveis
        ]

        return JsonResponse({"success": True, "alunos": alunos_data})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})





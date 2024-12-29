from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from srciencia_core.models.Turma import Turma, TurmaAluno
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

@login_required
def listar_alunos_turma(request, turma_id):
    try:
        alunos_visiveis = TurmaAluno.objects.filter(
            turma_id=turma_id, visivel=True
        ).select_related('aluno')
        
        alunos_data = [
            {
                "nome": aluno.aluno.get_full_name() or aluno.aluno.username,
                "email": aluno.aluno.email
            }
            for aluno in alunos_visiveis
        ]

        total_alunos = alunos_visiveis.count()  # Conta os alunos visíveis

        return JsonResponse({"success": True, "alunos": alunos_data, "total": total_alunos})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})










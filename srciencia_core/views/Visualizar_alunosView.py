from django.shortcuts import render, get_object_or_404
from srciencia_core.models import Turma
from django.http import JsonResponse


def alunos_turma_view(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    alunos = turma.aluno_set.all().values("nome", "email")
    return JsonResponse({"success": True, "alunos": list(alunos)})

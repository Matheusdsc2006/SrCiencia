from django.shortcuts import render, get_object_or_404
from srciencia_core.models import Turma
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def alunos_turma_view(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    alunos = turma.aluno_set.all()
    return render(request, 'alunos_turma.html', {'turma': turma, 'alunos': alunos})

@login_required
def listar_turmas_professor(request):
    turmas = Turma.objects.filter(professor=request.user).values(
        "id", "nome", "descricao", "codigo", "criado_em", "google_drive_url"
    ).order_by("-criado_em")

    return JsonResponse({"success": True, "turmas": list(turmas)})



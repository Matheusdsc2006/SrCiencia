from django.shortcuts import get_object_or_404, redirect
from srciencia_core.models import Turma

def excluir_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    turma.delete()
    return redirect('professor_turmas')

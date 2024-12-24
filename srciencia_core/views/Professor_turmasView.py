from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from srciencia_core.models import Turma
import random
import string
from django.http import HttpResponseForbidden


@login_required
def professor_turmas(request):
    # Verifica se o usuário é professor
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado para alunos.")

    turmas = Turma.objects.filter(professor=request.user).order_by("-criado_em")

    turmas_com_dados = [
        {
            "id": turma.id,
            "nome": turma.nome,
            "descricao": turma.descricao,
            "codigo": turma.codigo,
        }
        for turma in turmas
    ]

    return render(request, "professor_turmas.html", {"turmas": turmas_com_dados})


@login_required
def listar_turmas_professor(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso negado para alunos.")

    turmas = Turma.objects.filter(professor=request.user).values(
        "id", "nome", "descricao", "codigo", "professor__username"
    ).order_by("-criado_em")

    return JsonResponse({"success": True, "turmas": list(turmas)})


@login_required
def criar_turma(request):
    if request.method == "POST":
        nome = request.POST.get("class_name")
        descricao = request.POST.get("class_description", "")
        if not nome:
            return JsonResponse({"success": False, "message": "O nome da turma é obrigatório."})

        # Gerar código único para a turma
        codigo = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

        turma = Turma.objects.create(
            nome=nome,
            descricao=descricao,
            codigo=codigo,
            professor=request.user,
        )

        return JsonResponse({
            "success": True,
            "message": "Turma criada com sucesso.",
            "codigo": turma.codigo,
        })

    return JsonResponse({"success": False, "message": "Método inválido."})



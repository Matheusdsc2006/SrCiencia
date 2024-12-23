from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from srciencia_core.models import Turma
import random
import string

@login_required
def professor_turmas(request):
    if not request.user.is_staff:
        raise PermissionDenied

    turmas = Turma.objects.filter(professor=request.user)

    return render(request, "professor_turmas.html", {"turmas": turmas})

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



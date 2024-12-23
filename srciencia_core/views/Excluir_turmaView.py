from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from srciencia_core.models import Turma
import json

@login_required
def excluir_turma(request, id):
    if request.method == "POST":
        try:
            # Carregar o corpo da requisição
            body = json.loads(request.body.decode("utf-8"))
            senha = body.get("senha", "")

            # Validar a senha do usuário
            if not request.user.check_password(senha):
                return JsonResponse({"success": False, "message": "Senha incorreta."})

            # Obter a turma e excluir
            turma = get_object_or_404(Turma, id=id, professor=request.user)
            turma.delete()

            return JsonResponse({"success": True, "message": "Turma excluída com sucesso."})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Erro ao processar os dados enviados."})

    return JsonResponse({"success": False, "message": "Método inválido."})



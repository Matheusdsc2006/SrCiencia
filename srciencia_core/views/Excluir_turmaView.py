from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from srciencia_core.models import Turma
import json

@login_required
def excluir_turma(request, id):
    # Verifique o perfil do usuário
    if not request.user.perfil == 3:  # 3 indica o perfil de professor
        return JsonResponse({"success": False, "message": "Apenas professores podem excluir turmas."})

    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            senha = body.get("senha", "")
            if not request.user.check_password(senha):
                return JsonResponse({"success": False, "message": "Senha incorreta."})

            turma = get_object_or_404(Turma, id=id, professor=request.user)
            turma.delete()
            return JsonResponse({"success": True, "message": "Turma excluída com sucesso."})
        except Turma.DoesNotExist:
            return JsonResponse({"success": False, "message": "Turma não encontrada."})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Erro inesperado: {str(e)}"})

    return JsonResponse({"success": False, "message": "Método inválido."})


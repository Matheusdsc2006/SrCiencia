from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from srciencia_core.models import Turma
import json

@login_required
def excluir_turma(request, id):
    if not request.user.is_staff:
        return JsonResponse({"success": False, "message": "Apenas professores podem excluir turmas."})

    if request.method == "POST":
        try:
            # Carregar o corpo da requisição
            body = json.loads(request.body.decode("utf-8"))
            senha = body.get("senha", "")

            # Validar a senha do usuário
            if not request.user.check_password(senha):
                return JsonResponse({"success": False, "message": "Senha incorreta."})

            # Obter a turma e verificar se o professor é o proprietário
            turma = get_object_or_404(Turma, id=id, professor=request.user)

            # Excluir a turma
            turma.delete()

            return JsonResponse({"success": True, "message": "Turma excluída com sucesso."})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Erro ao processar os dados enviados."})
        except Turma.DoesNotExist:
            return JsonResponse({"success": False, "message": "Turma não encontrada."})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Erro inesperado: {str(e)}"})

    return JsonResponse({"success": False, "message": "Método inválido."})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from srciencia_core.models import Turma
import json

def verificar_codigo_turma(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            codigo_turma = data.get("codigo_turma")

            if not codigo_turma:
                return JsonResponse({"success": False, "message": "O código da turma é obrigatório."})

            # Buscar a turma pelo código
            turma = get_object_or_404(Turma, codigo=codigo_turma)

            # Adicionar o aluno à turma
            if turma.alunos.filter(id=request.user.id).exists():
                return JsonResponse({"success": False, "message": "Você já está inscrito nesta turma."})

            turma.alunos.add(request.user)
            turma.save()

            # Retornar os dados da turma, incluindo o professor
            return JsonResponse({
                "success": True,
                "message": "Você foi adicionado à turma.",
                "turma": {
                    "id": turma.id,
                    "nome": turma.nome,
                    "descricao": turma.descricao,
                    "codigo": turma.codigo,
                    "professor__username": turma.professor.username,
                }
            })
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Erro: {str(e)}"})
    return JsonResponse({"success": False, "message": "Método inválido."})

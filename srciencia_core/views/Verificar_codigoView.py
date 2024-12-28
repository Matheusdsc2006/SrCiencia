from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from srciencia_core.models.Turma import Turma, TurmaAluno
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

            # Verificar se o aluno já está inscrito na turma
            turma_aluno, created = TurmaAluno.objects.get_or_create(
                aluno=request.user, turma=turma
            )

            if not created:
                # Caso já exista, torná-la visível novamente
                turma_aluno.visivel = True
                turma_aluno.save()

                return JsonResponse({
                    "success": True,
                    "message": "Você já estava inscrito nesta turma. Ela foi exibida novamente.",
                    "turma": {
                        "id": turma.id,
                        "nome": turma.nome,
                        "descricao": turma.descricao,
                        "codigo": turma.codigo,
                        "professor__username": turma.professor.username if turma.professor else "Desconhecido",
                    }
                })

            # Se foi uma nova inscrição
            turma_aluno.visivel = True
            turma_aluno.save()

            return JsonResponse({
                "success": True,
                "message": "Você foi adicionado à turma.",
                "turma": {
                    "id": turma.id,
                    "nome": turma.nome,
                    "descricao": turma.descricao,
                    "codigo": turma.codigo,
                    "professor__username": turma.professor.username if turma.professor else "Desconhecido",
                }
            })

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Erro: {str(e)}"})

    return JsonResponse({"success": False, "message": "Método inválido."})

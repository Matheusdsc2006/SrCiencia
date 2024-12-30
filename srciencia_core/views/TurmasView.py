from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from srciencia_core.models.Turma import Turma, TurmaAluno

@login_required
def turmas_view(request):
    if request.user.is_staff:
        # Para professores, renderizar uma página personalizada
        turmas = Turma.objects.filter(professor=request.user)
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

    # Para alunos, exibir apenas turmas em que estão inscritos
    conta_atual = request.session.get("conta_atual", request.user.email)
    turmas = TurmaAluno.objects.filter(aluno=request.user, visivel=True).select_related("turma", "turma__professor")
    turmas_com_dados = [
        {
            "id": turma.turma.id,
            "nome": turma.turma.nome,
            "descricao": turma.turma.descricao,
            "professor__username": turma.turma.professor.username if turma.turma.professor else "Desconhecido",
        }
        for turma in turmas
    ]

    return render(request, "turmas.html", {
        "turmas": turmas_com_dados,
        "conta_atual": conta_atual,
    })

@login_required
def listar_turmas(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "Usuário não autenticado."})

    turmas = Turma.objects.filter(
        aluno=request.user,
        visivel=True  # Filtra apenas turmas visíveis
    ).select_related("turma", "turma__professor").values(
        "turma__id", "turma__nome", "turma__descricao", "turma__professor__username"
    )

    return JsonResponse({"success": True, "turmas": list(turmas)})

def mudar_conta(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            nova_conta = body.get("nova_conta")

            if nova_conta:
                # Obter o modelo de usuário personalizado
                User = get_user_model()

                # Verificar se o email pertence a um usuário cadastrado
                if not User.objects.filter(email=nova_conta).exists():
                    return JsonResponse({"success": False, "message": "Conta não encontrada. Cadastre-se antes de adicioná-la."})

                # Atualizar a conta atual na sessão
                request.session["conta_atual"] = request.session.get("conta_atual", nova_conta)
                request.session.modified = True

                # Atualizar a lista de contas, sem duplicar
                contas = request.session.get("contas", [])
                if nova_conta not in contas:
                    contas.append(nova_conta)

                # Marcar a última conta adicionada
                request.session["ultima_conta_adicionada"] = nova_conta
                request.session["contas"] = contas

                return JsonResponse({
                    "success": True, 
                    "message": "Conta adicionada com sucesso.",
                    "nova_conta": nova_conta
                })

            return JsonResponse({"success": False, "message": "Nenhuma conta fornecida."})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Erro interno: {str(e)}"})

    return JsonResponse({"success": False, "message": "Método inválido."})

def remover_conta(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        conta = body.get("conta")
        contas = request.session.get("contas", [])
        conta_atual = request.session.get("conta_atual")
        ultima_conta_adicionada = request.session.get("ultima_conta_adicionada")

        # Garantir que a conta fornecida esteja nas contas
        if conta not in contas:
            return JsonResponse({"success": False, "message": "Conta não encontrada."})

        # Impedir remoção da última conta adicionada
        if conta == ultima_conta_adicionada:
            return JsonResponse({"success": False, "message": "Você não pode remover uma conta que acabou de adicionar. Para isso, adicione outra conta."})

        # Caso a conta seja a atual, exigir confirmação de remoção
        if conta == conta_atual:
            return JsonResponse({
                "success": False,
                "message": "Confirme a remoção da conta atual."
            })

        # Remover a conta, caso seja diferente da atual
        contas.remove(conta)
        request.session["contas"] = contas
        request.session.modified = True  # Garantir que a sessão seja atualizada

        # Limpar última conta adicionada, se for removida
        if conta == ultima_conta_adicionada:
            request.session["ultima_conta_adicionada"] = None

        return JsonResponse({"success": True, "message": "Conta removida com sucesso."})

    return JsonResponse({"success": False, "message": "Método inválido."})

def listar_contas(request):
    contas = request.session.get("contas", [])
    conta_atual = request.session.get("conta_atual", request.user.email)

    if conta_atual not in contas:
        contas.append(conta_atual)
        request.session["contas"] = contas

    return JsonResponse({
        "success": True,
        "contas": contas,
        "conta_atual": conta_atual
    })


def pendentes_view(request, turma_id):
    return render(request, "paginas/pendentes.html", {"turma_id": turma_id})

@login_required
def cancelar_inscricao(request, turma_id):
    if request.method == "POST":
        try:
            turma_aluno = TurmaAluno.objects.get(aluno=request.user, turma_id=turma_id)
            turma_aluno.visivel = False  # Torna a turma invisível
            turma_aluno.save()
            return JsonResponse({"success": True, "message": "Inscrição cancelada com sucesso."})
        except TurmaAluno.DoesNotExist:
            return JsonResponse({"success": False, "message": "Você não está inscrito nesta turma."})
    return JsonResponse({"success": False, "message": "Método inválido."})

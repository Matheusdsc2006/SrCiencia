from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from srciencia_core.models import Turma


@login_required
def turmas_view(request):
    # Verificar se o usuário é um aluno (não professor)
    if request.user.is_staff:
        return HttpResponseForbidden("Acesso negado para professores.")

    # Obter a conta atual da sessão
    conta_atual = request.session.get("conta_atual")
    if not conta_atual:
        return render(request, "turmas.html", {"turmas": [], "conta_atual": "Nenhuma conta selecionada"})

    # Filtrar turmas associadas ao usuário (aluno)
    turmas = Turma.objects.filter(alunos=request.user).select_related("professor").order_by("-criado_em")

    # Adicionar professor ao contexto
    turmas_com_dados = [
        {
            "id": turma.id,
            "nome": turma.nome,
            "descricao": turma.descricao,
            "professor__username": turma.professor.username if turma.professor else "Desconhecido",
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

    turmas = Turma.objects.filter(alunos=request.user).select_related("professor").values(
        "id", "nome", "descricao", "professor__username", "google_drive_url"
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

                return JsonResponse({"success": True, "message": "Conta adicionada com sucesso.", "nova_conta": nova_conta})

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
    conta_atual = request.session.get("conta_atual", "Nenhuma conta selecionada")

    # Adicionar a conta atual à lista, se não estiver
    if conta_atual not in contas and conta_atual != "Nenhuma conta selecionada":
        contas.append(conta_atual)
        request.session["contas"] = contas  # Atualizar a sessão

    return JsonResponse({"contas": contas, "conta_atual": conta_atual})



def pendentes_view(request, turma_id):
    return render(request, "paginas/pendentes.html", {"turma_id": turma_id})


def cancelar_inscricao(request, turma_id):
    return redirect("turmas")

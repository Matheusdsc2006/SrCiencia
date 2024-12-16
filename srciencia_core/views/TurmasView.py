from django.shortcuts import render, redirect
from django.http import JsonResponse
import json


def turmas_view(request):
    conta_atual = request.session.get("conta_atual", None)
    contas = request.session.get("contas", ["oi@gmail.com"])

    TURMAS_POR_CONTA = {
        "usuario1@gmail.com": [{"id": 1, "nome": "Física II", "descricao": "Informática para Internet - 2M", "professor": "Israel França", "cor": "astronomia"}],
        "usuario2@gmail.com": [{"id": 2, "nome": "Biologia I", "descricao": "Controle Ambiental - 3M", "professor": "Gilsilene Ribeiro", "cor": "biologia"}],
    }

    # Carrega as turmas para a conta atual
    turmas = TURMAS_POR_CONTA.get(conta_atual, [])

    return render(request, "turmas.html", {"turmas": turmas, "conta_atual": conta_atual, "contas": contas})


def mudar_conta(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            nova_conta = body.get("nova_conta")

            if nova_conta:
                # Atualizar a conta na sessão
                request.session["conta_atual"] = nova_conta
                request.session.modified = True

                # Atualizar a lista de contas
                contas = request.session.get("contas", [])
                if nova_conta not in contas:
                    contas.append(nova_conta)
                request.session["contas"] = contas

                return JsonResponse({"success": True, "message": "Conta alterada com sucesso.", "nova_conta": nova_conta})

            return JsonResponse({"success": False, "message": "Nenhuma conta fornecida."})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Erro interno: {str(e)}"})

    return JsonResponse({"success": False, "message": "Método inválido."})


def remover_conta(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            conta_para_remover = body.get("conta")

            if conta_para_remover:
                contas = request.session.get("contas", [])
                if conta_para_remover in contas:
                    contas.remove(conta_para_remover)
                    request.session["contas"] = contas
                    if request.session.get("conta_atual") == conta_para_remover:
                        request.session["conta_atual"] = None
                    request.session.modified = True
                    return JsonResponse({"success": True, "message": "Conta removida com sucesso."})

                return JsonResponse({"success": False, "message": "Conta não encontrada."})

            return JsonResponse({"success": False, "message": "Nenhuma conta fornecida."})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Erro interno: {str(e)}"})

    return JsonResponse({"success": False, "message": "Método inválido."})



def listar_contas(request):
    contas = request.session.get("contas", [])
    conta_atual = request.session.get("conta_atual", "Nenhuma conta selecionada")
    return JsonResponse({"contas": contas, "conta_atual": conta_atual})


def pendentes_view(request, turma_id):
    return render(request, "paginas/pendentes.html", {"turma_id": turma_id})


def cancelar_inscricao(request, turma_id):
    return redirect("turmas")

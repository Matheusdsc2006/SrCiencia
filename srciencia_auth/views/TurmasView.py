from django.shortcuts import render, redirect
from django.http import JsonResponse    

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
        nova_conta = request.POST.get("nova_conta") or request.body.decode("utf-8").split("=")[-1]

        if nova_conta:
            # Atualizar a conta na sessão
            request.session["conta_atual"] = nova_conta
            request.session.modified = True  # Garante que a sessão seja salva

            # Atualizar a lista de contas na sessão e remover "oi@gmail.com"
            contas = request.session.get("contas", ["oi@gmail.com"])
            if "oi@gmail.com" in contas:
                contas.remove("oi@gmail.com")
            if nova_conta not in contas:
                contas.append(nova_conta)
            request.session["contas"] = contas

            # Retornar o email diretamente para o frontend
            return JsonResponse({"success": True, "message": f"Conta alterada para {nova_conta}.", "nova_conta": nova_conta})

    return JsonResponse({"success": False, "message": "Erro ao alterar a conta."})

def listar_contas(request):
    # Obter as contas da sessão
    contas = request.session.get("contas", [])
    conta_atual = request.session.get("conta_atual", "Nenhuma conta selecionada")

    # Retornar as contas e a conta atual em JSON
    return JsonResponse({"contas": contas, "conta_atual": conta_atual})


def pendentes_view(request, turma_id):
    return render(request, "paginas/pendentes.html", {"turma_id": turma_id})

def cancelar_inscricao(request, turma_id):
    # Simulação de lógica para cancelar inscrição
    return redirect("turmas")

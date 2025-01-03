from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from srciencia_core.models.Turma import Turma, TurmaAluno, Arquivo
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

@login_required
def turmas_view(request):
    if request.user.perfil == 3: 
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
    
    elif request.user.perfil == 2:  
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
    
    return redirect('pagina_inicial')


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
                User = get_user_model()

                # Verificar se o email pertence a um usuário cadastrado
                if not User.objects.filter(email=nova_conta).exists():
                    return JsonResponse({"success": False, "message": "Conta não encontrada. Cadastre-se antes de adicioná-la."})

                # Atualizar a lista de contas, sem duplicar
                contas = request.session.get("contas", [])
                if nova_conta not in contas:
                    contas.append(nova_conta)
                    request.session["contas"] = contas
                    request.session.modified = True

                # Não altera a conta atual aqui. Apenas adiciona à lista.
                return JsonResponse({"success": True, "message": "Conta adicionada com sucesso."})

            return JsonResponse({"success": False, "message": "Nenhuma conta fornecida."})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Erro interno: {str(e)}"})

    return JsonResponse({"success": False, "message": "Método inválido."})

@login_required
def confirmar_mudanca_conta(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            nova_conta = body.get("nova_conta")

            if nova_conta:
                contas = request.session.get("contas", [])
                if nova_conta not in contas:
                    return JsonResponse({"success": False, "message": "Conta não encontrada na lista. Adicione-a primeiro."})

                request.session["conta_atual"] = nova_conta
                request.session.modified = True

                return JsonResponse({"success": True, "message": "Conta atual alterada com sucesso."})

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

@require_POST
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

@require_POST
@login_required
def listar_anexos_pendentes(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
        turma_id = body.get("turma_id")

        if turma_id:
            turma = get_object_or_404(Turma, id=turma_id, alunos=request.user)
            anexos_nao_vistos = turma.arquivos.exclude(visualizado_por=request.user)

            pendentes = {
                "turma_id": turma.id,  # Certifique-se de incluir o ID da turma
                "turma": turma.nome,
                "professor": turma.professor.username if turma.professor else "Desconhecido",
                "anexos": [
                    {
                        "id": anexo.id,
                        "nome": anexo.nome,
                        "url": anexo.arquivo.url,
                        "data_hora": anexo.data_hora_formatada(),
                        "tamanho": anexo.tamanho_formatado(),
                    }
                    for anexo in anexos_nao_vistos
                ],
            }

            return JsonResponse({"success": True, "pendentes": pendentes})

        else:
            turmas = Turma.objects.filter(alunos=request.user)
            pendentes = []

            for turma in turmas:
                anexos_nao_vistos = turma.arquivos.exclude(visualizado_por=request.user)
                if anexos_nao_vistos.exists():
                    pendentes.append({
                        "turma_id": turma.id,  # Inclua o ID da turma aqui
                        "turma": turma.nome,
                        "professor": turma.professor.username if turma.professor else "Desconhecido",
                        "anexos": [
                            {
                                "id": anexo.id,
                                "nome": anexo.nome,
                                "url": anexo.arquivo.url,
                                "data_hora": anexo.data_hora_formatada(),
                                "tamanho": anexo.tamanho_formatado(),
                            }
                            for anexo in anexos_nao_vistos
                        ],
                    })

            return JsonResponse({"success": True, "pendentes": pendentes})

    except Turma.DoesNotExist:
        return JsonResponse({"success": False, "message": "Turma não encontrada."})
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Erro interno: {str(e)}"})


@require_POST
@login_required
@csrf_exempt
def marcar_arquivo_como_visto(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            arquivo_id = data.get("arquivo_id")
            if not arquivo_id:
                return JsonResponse({"success": False, "message": "ID do arquivo não fornecido."})

            arquivo = get_object_or_404(Arquivo, id=arquivo_id)

            # Adicionar o usuário ao campo `visualizado_por`
            arquivo.visualizado_por.add(request.user)
            arquivo.save()

            return JsonResponse({"success": True, "message": "Arquivo marcado como visto."})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Método inválido."})



    



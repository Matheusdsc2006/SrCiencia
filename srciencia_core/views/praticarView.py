from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from srciencia_core.models.Questao import Questao, Disciplina, Alternativa
from srciencia_core.models.Praticar import RespostaAluno, RelatorioQuestao
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, IntegerField
from django.db.models import OuterRef, Subquery
from difflib import SequenceMatcher
from random import sample
from random import shuffle
import random
from django.shortcuts import get_object_or_404
from django.db.models import Q
import json

@login_required
def aluno_praticar(request):
    """
    Renderiza a página de prática para o aluno.
    """
    disciplinas = Disciplina.objects.all()  
    return render(request, 'aluno_praticar.html', {
        'disciplinas': disciplinas,  
        'conteudos': [],   
        'topicos': [],    
    })

@login_required
def buscar_questoes(request):
    """
    Endpoint para buscar questões com base em filtros aplicados.
    """
    if request.method == 'GET':
        try:
            # Obtendo parâmetros de busca e filtros
            disciplina_id = request.GET.get('disciplina')
            conteudo_id = request.GET.get('conteudo')
            dificuldade = request.GET.get('dificuldade')
            quantidade = request.GET.get('quantidade', '10')  # Padrão: 10 questões
            status_filtros = request.GET.getlist('status', [])  # Lista de status
            busca = request.GET.get('busca', '').strip()  # Texto de busca

            print(f"Filtros recebidos: disciplina={disciplina_id}, conteudo={conteudo_id}, "
                  f"dificuldade={dificuldade}, quantidade={quantidade}, status={status_filtros}, busca={busca}")

            # Validar quantidade
            if not quantidade.isdigit() or int(quantidade) <= 0:
                raise ValueError("O parâmetro 'quantidade' deve ser um número inteiro positivo.")
            quantidade = int(quantidade)

            # Base inicial de questões
            questoes = Questao.objects.select_related(
                'banca', 'disciplina', 'conteudo', 'topico'
            ).all()
            print(f"Total de questões no banco: {questoes.count()}")

            # Aplicar filtros básicos
            if disciplina_id:
                questoes = questoes.filter(disciplina_id=disciplina_id)
                print(f"Após filtro disciplina: {questoes.count()}")
            if conteudo_id:
                questoes = questoes.filter(conteudo_id=conteudo_id)
                print(f"Após filtro conteúdo: {questoes.count()}")
            if dificuldade:
                questoes = questoes.filter(dificuldade=dificuldade)
                print(f"Após filtro dificuldade: {questoes.count()}")

            # Filtrar por status
            if 'nao_resolvidas' in status_filtros:
                # Excluir questões já respondidas
                questoes = questoes.exclude(respostas__aluno=request.user)
                print(f"Filtro 'não resolvidas' aplicado. Total após filtro: {questoes.count()}")
            else:
                # Nenhuma exclusão deve ocorrer
                print("Filtro 'não resolvidas' não aplicado. Exibindo todas as questões.")

            # Garantir que apenas filtros válidos sejam aplicados
            if 'que_errei' in status_filtros:
                questoes = questoes.filter(
                    respostas__aluno=request.user,
                    respostas__correta=False
                )
                print(f"Filtro 'que errei' aplicado. Total após filtro: {questoes.count()}")
            if 'com_resolucao' in status_filtros:
                questoes = questoes.filter(
                    Q(resolucao__isnull=False) & ~Q(resolucao="")
                )
                print(f"Filtro 'com resolução' aplicado. Total após filtro: {questoes.count()}")


            # Filtro de busca textual
            if busca:
                # Filtrar questões contendo o texto buscado no campo 'descricao'
                questoes = questoes.filter(descricao__icontains=busca)
                print(f"Questões encontradas por busca direta: {questoes.count()}")
            else:
                print("Nenhuma busca aplicada. Exibindo todas as questões.")



            # Embaralhar e limitar quantidade
            questoes = list(questoes)
            shuffle(questoes)
            questoes = questoes[:quantidade]
            print(f"Questões finais após embaralhar e limitar: {len(questoes)}")
            print(f"Parâmetros recebidos no backend: {request.GET}")

            # Serializar as questões para envio
            data = [
                {
                    'id': q.id,
                    'descricao': q.descricao,
                    'alternativas': list(q.alternativas.values('id', 'descricao', 'correta')),
                    'resolucao': q.resolucao,
                    'ano': q.ano,
                    'banca': q.banca.nome if q.banca else None,
                    'disciplina': q.disciplina.nome if q.disciplina else None,
                    'conteudo': q.conteudo.nome if q.conteudo else None,
                    'topico': q.topico.nome if q.topico else None,
                }
                for q in questoes
            ]

            return JsonResponse({'questoes': data})

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")
            return JsonResponse({'error': f'Erro inesperado: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
@login_required
def registrar_resposta(request):
    """
    Registra a resposta do aluno a uma questão.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            questao_id = data.get('questao_id')
            alternativa_id = data.get('alternativa_id')
            aluno = request.user

            # Verifica se a questão existe
            questao = Questao.objects.get(id=questao_id)

            # Verifica se a alternativa é correta
            alternativa_correta = questao.alternativas.filter(id=alternativa_id, correta=True).exists()

            # Registra a resposta do aluno
            RespostaAluno.objects.create(
                aluno=aluno,
                questao=questao,
                alternativa_id=alternativa_id,
                correta=alternativa_correta
            )

            return JsonResponse({'success': True, 'correta': alternativa_correta})

        except Questao.DoesNotExist:
            return JsonResponse({'error': 'Questão não encontrada'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método não permitido'}, status=405)


@csrf_exempt
@login_required
def reportar_questao(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            questao_id = data.get('questao_id')
            descricao = data.get('descricao')

            if not questao_id or not descricao:
                return JsonResponse({'error': 'Dados insuficientes para o relatório.'}, status=400)

            questao = Questao.objects.get(id=questao_id)

            # Criar o relatório
            RelatorioQuestao.objects.create(
                questao=questao,
                aluno=request.user,
                descricao_problema=descricao
            )

            return JsonResponse({'message': 'Relatório enviado com sucesso!'})

        except Questao.DoesNotExist:
            return JsonResponse({'error': 'Questão não encontrada.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Erro inesperado: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método não permitido.'}, status=405)

@csrf_exempt
@login_required
def finalizar_atividade(request):
    if request.method == 'POST':
        try:
            respostas = json.loads(request.body)
            aluno = request.user
            questoes_resolvidas = []

            for resposta in respostas:
                questao_id = resposta.get('questao_id')
                alternativa_id = resposta.get('alternativa_id')

                if not questao_id or not alternativa_id:
                    continue

                questao = Questao.objects.get(id=questao_id)
                alternativa = questao.alternativas.get(id=alternativa_id)
                correta = alternativa.correta

                # Salvar ou atualizar a resposta do aluno
                resposta_aluno, _ = RespostaAluno.objects.update_or_create(
                    aluno=aluno,
                    questao=questao,
                    defaults={
                        'alternativa_selecionada': alternativa,
                        'correta': correta,
                    },
                )

                # Adicionar a questão ao resumo
                questoes_resolvidas.append({
                    'id': questao.id,
                    'descricao': questao.descricao,
                    'alternativas': list(questao.alternativas.values('id', 'descricao', 'correta')),
                    'alternativa_selecionada': alternativa.id,
                    'resolucao': questao.resolucao or "",  # Inclui a resolução
                })

            return JsonResponse({
                'message': 'Atividade finalizada com sucesso!',
                'questoes_resolvidas': questoes_resolvidas,
            })

        except Exception as e:
            return JsonResponse({'error': f'Erro inesperado: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método não permitido.'}, status=405)



@csrf_exempt
@login_required
def registrar_resposta(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            questao_id = data.get('questao_id')
            alternativa_id = data.get('alternativa_id')

            if not questao_id or not alternativa_id:
                return JsonResponse({'error': 'Questão ou alternativa inválida.'}, status=400)

            questao = Questao.objects.get(id=questao_id)
            alternativa = questao.alternativas.get(id=alternativa_id)
            correta = alternativa.correta

            # Salvar a resposta
            RespostaAluno.objects.update_or_create(
                aluno=request.user,
                questao=questao,
                defaults={'alternativa_selecionada': alternativa, 'correta': correta},
            )

            return JsonResponse({'message': 'Resposta registrada com sucesso!', 'correta': correta})

        except Questao.DoesNotExist:
            return JsonResponse({'error': 'Questão não encontrada.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Erro inesperado: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método não permitido.'}, status=405)



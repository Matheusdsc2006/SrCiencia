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

import random
from difflib import SequenceMatcher
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def buscar_questoes(request):
    if request.method == 'GET':
        try:
            # Obtendo filtros
            disciplina_id = request.GET.get('disciplina')
            conteudo_id = request.GET.get('conteudo')
            dificuldade = request.GET.get('dificuldade')
            quantidade = request.GET.get('quantidade', '10')  # Padrão: 10 questões
            status_filtros = request.GET.getlist('status', [])  # Lista de status
            busca = request.GET.get('busca', '').strip()  # Busca textual

            # Validação de quantidade
            if not quantidade.isdigit() or int(quantidade) <= 0:
                raise ValueError("O parâmetro 'quantidade' deve ser um número inteiro positivo.")
            quantidade = int(quantidade)

            # Base inicial de questões
            questoes = Questao.objects.select_related(
                'banca', 'disciplina', 'conteudo', 'topico'
            ).all()

            # Aplicando filtros
            if disciplina_id:
                questoes = questoes.filter(disciplina_id=disciplina_id)
            if conteudo_id:
                questoes = questoes.filter(conteudo_id=conteudo_id)
            if dificuldade:
                questoes = questoes.filter(dificuldade=dificuldade)

            # Subquery para identificar questões já respondidas pelo aluno
            respostas_subquery = RespostaAluno.objects.filter(
                aluno=request.user,
                questao=OuterRef('pk')
            ).values('id')

            # Filtrar questões pelo status
            if 'nao_resolvidas' in status_filtros:
                questoes = questoes.annotate(respondida=Subquery(respostas_subquery[:1])).filter(respondida__isnull=True)
            if 'com_resolucao' in status_filtros:
                questoes = questoes.filter(resolucao__isnull=False).exclude(resolucao="")
            if 'que_errei' in status_filtros:questoes = questoes.filter(respostas__aluno=request.user,respostas__correta=False)

            # Filtro de busca
            if busca:
                # Filtrar questões que contenham exatamente o termo buscado
                questoes_exatas = questoes.filter(descricao__icontains=busca)

                if questoes_exatas.exists():
                    questoes = questoes_exatas
                else:
                    # Calcular similaridade com difflib
                    questoes_similares = []
                    for questao in questoes:
                        similaridade = SequenceMatcher(None, busca, questao.descricao).ratio()
                        if similaridade > 0.3:  # Similaridade mínima de 30%
                            questoes_similares.append((similaridade, questao))

                    # Ordenar pela maior similaridade
                    questoes_similares.sort(key=lambda x: x[0], reverse=True)
                    questoes = [q[1] for q in questoes_similares]

            # Embaralhar as questões antes de limitar a quantidade
            questoes = list(questoes)  # Converte para lista para permitir embaralhamento
            random.shuffle(questoes)

            # Limitar quantidade de questões
            questoes = questoes[:quantidade]

            # Serializar resultados
            data = [
                {
                    'id': questao.id,
                    'descricao': questao.descricao,
                    'alternativas': list(questao.alternativas.values('id', 'descricao', 'correta')),
                    'resolucao': questao.resolucao,
                    'ano': questao.ano,
                    'banca': questao.banca.nome if questao.banca else None,
                    'disciplina': questao.disciplina.nome if questao.disciplina else None,
                    'conteudo': questao.conteudo.nome if questao.conteudo else None,
                    'topico': questao.topico.nome if questao.topico else None,
                }
                for questao in questoes
            ]
            return JsonResponse({'questoes': data})

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Erro inesperado: ' + str(e)}, status=500)

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

@login_required
def finalizar_atividade(request):
    if request.method == 'POST':
        respostas = request.POST.getlist('respostas', [])

        for resposta_data in respostas:
            questao_id = resposta_data.get('questao_id')
            alternativa_id = resposta_data.get('alternativa_id')

            # Obter a questão e a alternativa
            questao = get_object_or_404(Questao, id=questao_id)
            alternativa = get_object_or_404(Alternativa, id=alternativa_id)

            # Atualizar ou criar a resposta do aluno
            RespostaAluno.objects.update_or_create(
                aluno=request.user,
                questao=questao,
                defaults={
                    'alternativa_selecionada': alternativa,
                    'correta': alternativa.correta
                }
            )

        return JsonResponse({'message': 'Atividade finalizada com sucesso!'})
    return JsonResponse({'error': 'Método não permitido'}, status=405)

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
